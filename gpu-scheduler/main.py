#!/usr/bin/env python

import os
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

def bind_pod_to_node(v1, pod, node_name):
    try:
        # binding = client.V1Binding(
        #     metadata=client.V1ObjectMeta(name=pod.metadata.name, namespace=pod.metadata.namespace),
        #     target=client.V1ObjectReference(kind="Node", name=node_name)
        # )
        # v1.create_namespaced_binding(namespace=pod.metadata.namespace, body=binding)
        
        body=client.V1Binding()
        
        target=client.V1ObjectReference()
        target.kind="Node"
        target.apiVersion="v1"
        target.name=node_name
        
        meta=client.V1ObjectMeta()
        meta.name=pod.metadata.name
        
        body.target=target
        body.metadata=meta
        
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_binding
        res = v1.create_namespaced_binding(namespace=pod.metadata.namespace, body=binding, target=target )
        logger.info(f"Bound pod {pod.metadata.name} to {node_name}")
        logger.info(f"Res: {res}")
    except ApiException as e:
        logger.error(f"Failed to bind pod {pod.metadata.name} to {node_name}: {e}")

def patch_pod_env(v1, pod, cuda_devices):
    try:
        body = {
            "spec": {
                "containers": [{
                    "name": pod.spec.containers[0].name,
                    "env": [{"name": "CUDA_VISIBLE_DEVICES", "value": cuda_devices}]
                }]
            }
        }
        res = v1.patch_namespaced_pod(name=pod.metadata.name, namespace=pod.metadata.namespace, body=body)
        logger.info(f"Patched pod {pod.metadata.name} with CUDA_VISIBLE_DEVICES={cuda_devices}")
    except ApiException as e:
        logger.error(f"Failed to patch pod {pod.metadata.name}: {e}")

def main():
    try:
        config.load_incluster_config()
    except Exception as e:
        logger.error(f"Failed to load Kubernetes config: {e}")
        return

    v1 = client.CoreV1Api()
    # scheduler_name = os.getenv("SCHEDULER_NAME", "gpu-scheduler")
    w = watch.Watch()
    
    logger.info(f"Scheduler running, client: {v1}, watch: {w}")

    for event in w.stream(v1.list_namespaced_pod, namespace="default", field_selector=f"spec.schedulerName=gpu-scheduler,status.phase=Pending"):
        pod = event['object']
        try:
            # if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
                # logger.info(f"Pod {pod.metadata.name} already scheduled, skipping")
            
            if pod.spec.node_name:
                # logger.info(f"Pod {pod.metadata.name} already scheduled, skipping")
                continue

            # if not pod.status.phase == "Pending":
            #     # logger.info(f"Pod {pod.metadata.name} status: {pod.status.phase} != Pending, skipping")
            #     continue
            # else:
            #     logger.info(f"Pod {pod.metadata.name} status: {pod.status.phase}...")


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
            pod_idx = int(pod.metadata.name.split('-')[-1]) if pod.metadata.name else 0
            if pod_idx not in gpu_map:
                logger.warning(f"No GPU mapping for pod index {pod_idx} in pod {pod.metadata.name}")
                continue

            node_name = gpu_map[pod_idx]['node']
            cuda_devices = gpu_map[pod_idx]['cuda_devices']
            
            # we will patch before binding, this way pods won't be recreated after bind
            try:
                patch_pod_env(v1, pod, cuda_devices)
            except Exception as e:
                logger.error(f"Error patching pod {pod.metadata.name}: {e}")

            try:
                bind_pod_to_node(v1, pod, node_name)
            except Exception as e:
                # see https://github.com/kubernetes-client/python/issues/825#issuecomment-515676591
                # Invalid value for `target`, must not be `None`
                logger.error(f"Error binding pod {pod.metadata.name}: {e}")
            
                
        except Exception as e:
            logger.error(f"Error processing pod {pod.metadata.name}: {e}")

if __name__ == "__main__":
    main()