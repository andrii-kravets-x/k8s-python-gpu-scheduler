#!/usr/bin/env python

import os
import re
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from loguru import logger

def parse_gpu_map(gpu_map_str):
    gpu_map = {}
    try:
        for line in gpu_map_str.strip().split('\n'):
            pod_idx, node_info = line.split('=')
            node_name, cuda_devices = node_info.split(':')
            gpu_map[int(pod_idx)] = {'node': node_name, 'cuda_devices': cuda_devices}
    except Exception as e:
        logger.error(f"Error parsing gpu_map_str {pod_idx}: {e}")
    finally:
        return gpu_map

def bind_pod_to_node(core_v1_api, pod, node_name):
    try:
        logger.info(f"Trying to bind pod {pod.metadata.name}...")
        body = client.V1Binding(
            metadata=client.V1ObjectMeta(name=pod.metadata.name, namespace=pod.metadata.namespace),
            target=client.V1ObjectReference(kind="Node", name=node_name)
        )
        core_v1_api.create_namespaced_binding(namespace=pod.metadata.namespace, body=body)        

    except ApiException as e:
        logger.error(f"Failed to bind pod {pod.metadata.name} to {node_name}: {e}")
    except Exception as e:
        if str(e) == "Invalid value for `target`, must not be `None`":
            # see https://github.com/kubernetes-client/python/issues/825#issuecomment-515676591
            # pass  # Suppress this specific error

            pod_result = core_v1_api.read_namespaced_pod(name=pod.metadata.name, namespace=pod.metadata.namespace)
            logger.info(f"Bound pod {pod.metadata.name} to node: {pod_result.spec.node_name}")
        else:
            logger.error(f"Unexpected error while binding {pod.metadata.name}: {e}")
            raise  # Re-raise 

def patch_pod_env(core_v1_api, pod, cuda_devices):
    try:
        logger.info(f"Trying to patch pod {pod.metadata.name}...")
        body = {
            "metadata": {
                "annotations": {
                    "cuda": "CUDA_VISIBLE_DEVICES=" + cuda_devices
                }
            }
        }

        core_v1_api.patch_namespaced_pod(name=pod.metadata.name, namespace=pod.metadata.namespace, body=body)
        logger.info(f"Patched pod {pod.metadata.name} with CUDA_VISIBLE_DEVICES={cuda_devices}")
    except ApiException as e:
        logger.error(f"Failed to patch pod {pod.metadata.name}: {e}")

def main():
    try:
        config.load_incluster_config()
    except Exception as e:
        logger.error(f"Failed to load Kubernetes config: {e}")
        return

    # apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()
    w = watch.Watch()
    logger.info(f"Scheduler running, client: {core_v1_api}, watch: {w}")

    for event in w.stream(core_v1_api.list_namespaced_pod, namespace="default", field_selector=f"spec.schedulerName=gpu-scheduler,status.phase=Pending"):
        pod = event['object']
        try:
            if pod.spec.node_name:
                # logger.debug(f"Pod {pod.metadata.name} already scheduled, skipping")
                continue

            annotations = pod.metadata.annotations or {}
            gpu_map_str = annotations.get('gpu-scheduling-map', '')
            if not gpu_map_str:
                logger.warning(f"No gpu-scheduling-map annotation found for pod {pod.metadata.name}")
                continue

            gpu_map = parse_gpu_map(gpu_map_str)
            if not gpu_map:
                logger.warning(f"Invalid GPU map for pod {pod.metadata.name}")
                continue

            # logger.debug(f"pod: {pod}")
            # pod_idx = int(pod.metadata.name.split('-')[-1])
            match = re.search(r'-(\d+)$', pod.metadata.name)
            pod_idx = int(match.group(1)) if match else 0 # set pod id to 0 as a fallback
            if pod_idx not in gpu_map:
                logger.warning(f"No GPU mapping for pod index {pod_idx} in pod {pod.metadata.name}")
                continue

            node_name = gpu_map[pod_idx]['node']
            cuda_devices = gpu_map[pod_idx]['cuda_devices']
            
        except Exception as e:
            logger.error(f"Error processing pod {pod.metadata.name}: {e}")

        bind_pod_to_node(core_v1_api, pod, node_name)

        try:
            patch_pod_env(core_v1_api, pod, cuda_devices)
        except Exception as e:
            logger.error(f"Error patching pod {pod.metadata.name}: {e}")

if __name__ == "__main__":
    main()