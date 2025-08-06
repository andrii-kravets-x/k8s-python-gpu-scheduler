## Results
>Include in the repository the output of the command `kubectl get pod -owide -A` and the logs of pods located on node3 and node4.

#### logs of pods(gpu-scheduler-check only, w/o kindnet or kube-proxy) located on node3 and node4
```ruby
ubuntu@gpu-scheduler-kind ~/k8s-scheduler (main)> kubectl logs gpu-scheduler-check-2 --tail 3 
Pod name: gpu-scheduler-check-2, CUDA_VISIBLE_DEVICES: 0,1,2
Pod name: gpu-scheduler-check-2, CUDA_VISIBLE_DEVICES: 0,1,2
Pod name: gpu-scheduler-check-2, CUDA_VISIBLE_DEVICES: 0,1,2

ubuntu@gpu-scheduler-kind ~/k8s-scheduler (main)> kubectl logs gpu-scheduler-check-3 --tail 3
Pod name: gpu-scheduler-check-3, CUDA_VISIBLE_DEVICES: 3
Pod name: gpu-scheduler-check-3, CUDA_VISIBLE_DEVICES: 3
Pod name: gpu-scheduler-check-3, CUDA_VISIBLE_DEVICES: 3

ubuntu@gpu-scheduler-kind ~/k8s-scheduler (main)> kubectl logs gpu-scheduler-check-4 --tail 3
Pod name: gpu-scheduler-check-4, CUDA_VISIBLE_DEVICES: 3
Pod name: gpu-scheduler-check-4, CUDA_VISIBLE_DEVICES: 3
Pod name: gpu-scheduler-check-4, CUDA_VISIBLE_DEVICES: 3
```

#### `kubectl logs statefulsets/gpu-scheduler-check --all-pods=true -f --timestamps --max-log-requests 6`
```ruby
[pod/gpu-scheduler-check-0/gpu-scheduler-check] 2025-08-06T16:06:39.942843383Z Pod name: gpu-scheduler-check-0, CUDA_VISIBLE_DEVICES: 0,1
[pod/gpu-scheduler-check-1/gpu-scheduler-check] 2025-08-06T16:06:40.722801636Z Pod name: gpu-scheduler-check-1, CUDA_VISIBLE_DEVICES: 2
[pod/gpu-scheduler-check-2/gpu-scheduler-check] 2025-08-06T16:06:41.482433942Z Pod name: gpu-scheduler-check-2, CUDA_VISIBLE_DEVICES: 0,1,2
[pod/gpu-scheduler-check-3/gpu-scheduler-check] 2025-08-06T16:06:42.465334794Z Pod name: gpu-scheduler-check-3, CUDA_VISIBLE_DEVICES: 3
[pod/gpu-scheduler-check-4/gpu-scheduler-check] 2025-08-06T16:06:43.464767255Z Pod name: gpu-scheduler-check-4, CUDA_VISIBLE_DEVICES: 3
[pod/gpu-scheduler-check-0/gpu-scheduler-check] 2025-08-06T16:06:49.942984713Z Pod name: gpu-scheduler-check-0, CUDA_VISIBLE_DEVICES: 0,1
[pod/gpu-scheduler-check-1/gpu-scheduler-check] 2025-08-06T16:06:50.722955682Z Pod name: gpu-scheduler-check-1, CUDA_VISIBLE_DEVICES: 2
[pod/gpu-scheduler-check-2/gpu-scheduler-check] 2025-08-06T16:06:51.482507134Z Pod name: gpu-scheduler-check-2, CUDA_VISIBLE_DEVICES: 0,1,2
[pod/gpu-scheduler-check-3/gpu-scheduler-check] 2025-08-06T16:06:52.465524661Z Pod name: gpu-scheduler-check-3, CUDA_VISIBLE_DEVICES: 3
[pod/gpu-scheduler-check-4/gpu-scheduler-check] 2025-08-06T16:06:53.464892844Z Pod name: gpu-scheduler-check-4, CUDA_VISIBLE_DEVICES: 3
```

#### `kubectl get pod -owide -A`

```ruby
NAMESPACE            NAME                                         READY   STATUS    RESTARTS   AGE   IP           NODE                 NOMINATED NODE   READINESS GATES
default              gpu-scheduler-check-0                        1/1     Running   0          29s   10.244.5.2   node1                <none>           <none>
default              gpu-scheduler-check-1                        1/1     Running   0          29s   10.244.1.2   node2                <none>           <none>
default              gpu-scheduler-check-2                        1/1     Running   0          28s   10.244.3.2   node3                <none>           <none>
default              gpu-scheduler-check-3                        1/1     Running   0          27s   10.244.2.2   node4                <none>           <none>
default              gpu-scheduler-check-4                        1/1     Running   0          26s   10.244.2.3   node4                <none>           <none>
default              gpu-scheduler-check-5                        0/1     Pending   0          25s   <none>       <none>               <none>           <none>
kube-system          coredns-674b8bbfcf-c25bg                     1/1     Running   0          17m   10.244.0.2   kind-control-plane   <none>           <none>
kube-system          coredns-674b8bbfcf-h78gs                     1/1     Running   0          17m   10.244.0.3   kind-control-plane   <none>           <none>
kube-system          etcd-kind-control-plane                      1/1     Running   0          17m   172.18.0.6   kind-control-plane   <none>           <none>
kube-system          gpu-scheduler-77c89d4bfc-8lwx7               1/1     Running   0          70s   10.244.0.5   kind-control-plane   <none>           <none>
kube-system          kindnet-6mlhj                                1/1     Running   0          17m   172.18.0.5   node1                <none>           <none>
kube-system          kindnet-c9qwt                                1/1     Running   0          17m   172.18.0.3   node4                <none>           <none>
kube-system          kindnet-gcnfs                                1/1     Running   0          17m   172.18.0.2   node2                <none>           <none>
kube-system          kindnet-jjtgr                                1/1     Running   0          17m   172.18.0.4   node3                <none>           <none>
kube-system          kindnet-phcb4                                1/1     Running   0          17m   172.18.0.6   kind-control-plane   <none>           <none>
kube-system          kube-apiserver-kind-control-plane            1/1     Running   0          17m   172.18.0.6   kind-control-plane   <none>           <none>
kube-system          kube-controller-manager-kind-control-plane   1/1     Running   0          17m   172.18.0.6   kind-control-plane   <none>           <none>
kube-system          kube-proxy-9jwdr                             1/1     Running   0          17m   172.18.0.3   node4                <none>           <none>
kube-system          kube-proxy-c6tm2                             1/1     Running   0          17m   172.18.0.6   kind-control-plane   <none>           <none>
kube-system          kube-proxy-c8kpt                             1/1     Running   0          17m   172.18.0.2   node2                <none>           <none>
kube-system          kube-proxy-j6lhs                             1/1     Running   0          17m   172.18.0.4   node3                <none>           <none>
kube-system          kube-proxy-xtnlk                             1/1     Running   0          17m   172.18.0.5   node1                <none>           <none>
kube-system          kube-scheduler-kind-control-plane            1/1     Running   0          17m   172.18.0.6   kind-control-plane   <none>           <none>
local-path-storage   local-path-provisioner-7dc846544d-fm8tw      1/1     Running   0          17m   10.244.0.4   kind-control-plane   <none>           <none>
```

#### `kubectl get nodes`

```ruby
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   35s   v1.33.1
node1                Ready    <none>          25s   v1.33.1
node2                Ready    <none>          25s   v1.33.1
node3                Ready    <none>          25s   v1.33.1
node4                Ready    <none>          25s   v1.33.1
```

#### `kubectl logs -f deployments/gpu-scheduler -n kube-system`
```ruby
2025-08-06 16:01:40.099 | INFO     | __main__:main:69 - Scheduler running, client: <kubernetes.client.api.core_v1_api.CoreV1Api object at 0x76bde39b12b0>, watch: <kubernetes.watch.watch.Watch object at 0x76bde39b16a0>
2025-08-06 16:02:19.133 | INFO     | __main__:bind_pod_to_node:23 - Trying to bind pod gpu-scheduler-check-0...
2025-08-06 16:02:19.156 | INFO     | __main__:bind_pod_to_node:38 - Bound pod gpu-scheduler-check-0 to node: node1
2025-08-06 16:02:19.156 | INFO     | __main__:patch_pod_env:45 - Trying to patch pod gpu-scheduler-check-0...
2025-08-06 16:02:19.175 | INFO     | __main__:patch_pod_env:55 - Patched pod gpu-scheduler-check-0 with CUDA_VISIBLE_DEVICES=0,1
2025-08-06 16:02:19.930 | INFO     | __main__:bind_pod_to_node:23 - Trying to bind pod gpu-scheduler-check-1...
2025-08-06 16:02:19.948 | INFO     | __main__:bind_pod_to_node:38 - Bound pod gpu-scheduler-check-1 to node: node2
2025-08-06 16:02:19.949 | INFO     | __main__:patch_pod_env:45 - Trying to patch pod gpu-scheduler-check-1...
2025-08-06 16:02:19.964 | INFO     | __main__:patch_pod_env:55 - Patched pod gpu-scheduler-check-1 with CUDA_VISIBLE_DEVICES=2
2025-08-06 16:02:20.684 | INFO     | __main__:bind_pod_to_node:23 - Trying to bind pod gpu-scheduler-check-2...
2025-08-06 16:02:20.707 | INFO     | __main__:bind_pod_to_node:38 - Bound pod gpu-scheduler-check-2 to node: node3
2025-08-06 16:02:20.708 | INFO     | __main__:patch_pod_env:45 - Trying to patch pod gpu-scheduler-check-2...
2025-08-06 16:02:20.733 | INFO     | __main__:patch_pod_env:55 - Patched pod gpu-scheduler-check-2 with CUDA_VISIBLE_DEVICES=0,1,2
2025-08-06 16:02:21.674 | INFO     | __main__:bind_pod_to_node:23 - Trying to bind pod gpu-scheduler-check-3...
2025-08-06 16:02:21.692 | INFO     | __main__:bind_pod_to_node:38 - Bound pod gpu-scheduler-check-3 to node: node4
2025-08-06 16:02:21.692 | INFO     | __main__:patch_pod_env:45 - Trying to patch pod gpu-scheduler-check-3...
2025-08-06 16:02:21.707 | INFO     | __main__:patch_pod_env:55 - Patched pod gpu-scheduler-check-3 with CUDA_VISIBLE_DEVICES=3
2025-08-06 16:02:22.670 | INFO     | __main__:bind_pod_to_node:23 - Trying to bind pod gpu-scheduler-check-4...
2025-08-06 16:02:22.686 | INFO     | __main__:bind_pod_to_node:38 - Bound pod gpu-scheduler-check-4 to node: node4
2025-08-06 16:02:22.686 | INFO     | __main__:patch_pod_env:45 - Trying to patch pod gpu-scheduler-check-4...
2025-08-06 16:02:22.712 | INFO     | __main__:patch_pod_env:55 - Patched pod gpu-scheduler-check-4 with CUDA_VISIBLE_DEVICES=3
2025-08-06 16:02:23.674 | WARNING  | __main__:main:94 - No GPU mapping for pod index 5 in pod gpu-scheduler-check-5
```


#### `kubectl events -w -A`
```ruby
NAMESPACE   LAST SEEN   TYPE     REASON     OBJECT                    MESSAGE
default     16m         Normal   Starting   Node/kind-control-plane   Starting kubelet.
default     16m         Normal   NodeAllocatableEnforced   Node/kind-control-plane   Updated Node Allocatable limit across pods
default     16m         Normal   NodeHasSufficientMemory   Node/kind-control-plane   Node kind-control-plane status is now: NodeHasSufficientMemory
default     16m         Normal   NodeHasNoDiskPressure     Node/kind-control-plane   Node kind-control-plane status is now: NodeHasNoDiskPressure
default     16m         Normal   NodeHasSufficientPID      Node/kind-control-plane   Node kind-control-plane status is now: NodeHasSufficientPID
default     16m         Normal   RegisteredNode            Node/kind-control-plane   Node kind-control-plane event: Registered Node kind-control-plane in Controller
default     16m         Normal   Starting                  Node/kind-control-plane   
default     15m         Normal   NodeReady                 Node/kind-control-plane   Node kind-control-plane status is now: NodeReady
default     16m (x2 over 16m)   Normal   NodeHasSufficientMemory   Node/node1                Node node1 status is now: NodeHasSufficientMemory
default     16m (x2 over 16m)   Normal   NodeHasNoDiskPressure     Node/node1                Node node1 status is now: NodeHasNoDiskPressure
default     16m (x2 over 16m)   Normal   NodeHasSufficientPID      Node/node1                Node node1 status is now: NodeHasSufficientPID
default     16m                 Normal   NodeAllocatableEnforced   Node/node1                Updated Node Allocatable limit across pods
default     16m                 Normal   RegisteredNode            Node/node1                Node node1 event: Registered Node node1 in Controller
default     15m                 Normal   Starting                  Node/node1                
default     15m                 Normal   NodeReady                 Node/node1                Node node1 status is now: NodeReady
default     16m                 Normal   Starting                  Node/node2                Starting kubelet.
default     16m (x2 over 16m)   Normal   NodeHasSufficientMemory   Node/node2                Node node2 status is now: NodeHasSufficientMemory
default     16m (x2 over 16m)   Normal   NodeHasNoDiskPressure     Node/node2                Node node2 status is now: NodeHasNoDiskPressure
default     16m (x2 over 16m)   Normal   NodeHasSufficientPID      Node/node2                Node node2 status is now: NodeHasSufficientPID
default     16m                 Normal   NodeAllocatableEnforced   Node/node2                Updated Node Allocatable limit across pods
default     16m                 Normal   RegisteredNode            Node/node2                Node node2 event: Registered Node node2 in Controller
default     16m                 Normal   Starting                  Node/node2                
default     15m                 Normal   NodeReady                 Node/node2                Node node2 status is now: NodeReady
default     16m (x2 over 16m)   Normal   NodeHasSufficientMemory   Node/node3                Node node3 status is now: NodeHasSufficientMemory
default     16m (x2 over 16m)   Normal   NodeHasNoDiskPressure     Node/node3                Node node3 status is now: NodeHasNoDiskPressure
default     16m (x2 over 16m)   Normal   NodeHasSufficientPID      Node/node3                Node node3 status is now: NodeHasSufficientPID
default     16m                 Normal   NodeAllocatableEnforced   Node/node3                Updated Node Allocatable limit across pods
default     16m                 Normal   CIDRAssignmentFailed      Node/node3                Node node3 status is now: CIDRAssignmentFailed
default     16m                 Normal   RegisteredNode            Node/node3                Node node3 event: Registered Node node3 in Controller
default     15m                 Normal   Starting                  Node/node3                
default     15m                 Normal   NodeReady                 Node/node3                Node node3 status is now: NodeReady
default     16m (x2 over 16m)   Normal   NodeHasSufficientMemory   Node/node4                Node node4 status is now: NodeHasSufficientMemory
default     16m (x2 over 16m)   Normal   NodeHasNoDiskPressure     Node/node4                Node node4 status is now: NodeHasNoDiskPressure
default     16m (x2 over 16m)   Normal   NodeHasSufficientPID      Node/node4                Node node4 status is now: NodeHasSufficientPID
default     16m                 Normal   NodeAllocatableEnforced   Node/node4                Updated Node Allocatable limit across pods
default     16m                 Normal   RegisteredNode            Node/node4                Node node4 event: Registered Node node4 in Controller
default     15m                 Normal   Starting                  Node/node4                
default     15m                 Normal   NodeReady                 Node/node4                Node node4 status is now: NodeReady
kube-system   16m                 Warning   FailedScheduling          Pod/coredns-674b8bbfcf-c25bg   0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/not-ready: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
kube-system   15m                 Normal    Scheduled                 Pod/coredns-674b8bbfcf-c25bg   Successfully assigned kube-system/coredns-674b8bbfcf-c25bg to kind-control-plane
kube-system   15m                 Normal    Pulled                    Pod/coredns-674b8bbfcf-c25bg   Container image "registry.k8s.io/coredns/coredns:v1.12.0" already present on machine
kube-system   15m                 Normal    Created                   Pod/coredns-674b8bbfcf-c25bg   Created container: coredns
kube-system   15m                 Normal    Started                   Pod/coredns-674b8bbfcf-c25bg   Started container coredns
kube-system   16m                 Warning   FailedScheduling          Pod/coredns-674b8bbfcf-h78gs   0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/not-ready: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
kube-system   15m                 Normal    Scheduled                 Pod/coredns-674b8bbfcf-h78gs   Successfully assigned kube-system/coredns-674b8bbfcf-h78gs to kind-control-plane
kube-system   15m                 Normal    Pulled                    Pod/coredns-674b8bbfcf-h78gs   Container image "registry.k8s.io/coredns/coredns:v1.12.0" already present on machine
kube-system   15m                 Normal    Created                   Pod/coredns-674b8bbfcf-h78gs   Created container: coredns
kube-system   15m                 Normal    Started                   Pod/coredns-674b8bbfcf-h78gs   Started container coredns
kube-system   16m                 Normal    SuccessfulCreate          ReplicaSet/coredns-674b8bbfcf   Created pod: coredns-674b8bbfcf-h78gs
kube-system   16m                 Normal    SuccessfulCreate          ReplicaSet/coredns-674b8bbfcf   Created pod: coredns-674b8bbfcf-c25bg
kube-system   16m                 Normal    ScalingReplicaSet         Deployment/coredns              Scaled up replica set coredns-674b8bbfcf from 0 to 2
kube-system   16m                 Normal    Scheduled                 Pod/kindnet-6mlhj               Successfully assigned kube-system/kindnet-6mlhj to node1
kube-system   16m                 Normal    Pulled                    Pod/kindnet-6mlhj               Container image "docker.io/kindest/kindnetd:v20250512-df8de77b" already present on machine
kube-system   15m                 Normal    Created                   Pod/kindnet-6mlhj               Created container: kindnet-cni
kube-system   15m                 Normal    Started                   Pod/kindnet-6mlhj               Started container kindnet-cni
kube-system   16m                 Normal    Scheduled                 Pod/kindnet-c9qwt               Successfully assigned kube-system/kindnet-c9qwt to node4
kube-system   16m                 Normal    Pulled                    Pod/kindnet-c9qwt               Container image "docker.io/kindest/kindnetd:v20250512-df8de77b" already present on machine
kube-system   15m                 Normal    Created                   Pod/kindnet-c9qwt               Created container: kindnet-cni
kube-system   15m                 Normal    Started                   Pod/kindnet-c9qwt               Started container kindnet-cni
kube-system   16m                 Normal    Scheduled                 Pod/kindnet-gcnfs               Successfully assigned kube-system/kindnet-gcnfs to node2
kube-system   16m                 Normal    Pulled                    Pod/kindnet-gcnfs               Container image "docker.io/kindest/kindnetd:v20250512-df8de77b" already present on machine
kube-system   16m                 Normal    Created                   Pod/kindnet-gcnfs               Created container: kindnet-cni
kube-system   16m                 Normal    Started                   Pod/kindnet-gcnfs               Started container kindnet-cni
kube-system   16m                 Normal    Scheduled                 Pod/kindnet-jjtgr               Successfully assigned kube-system/kindnet-jjtgr to node3
kube-system   16m                 Normal    Pulled                    Pod/kindnet-jjtgr               Container image "docker.io/kindest/kindnetd:v20250512-df8de77b" already present on machine
kube-system   15m                 Normal    Created                   Pod/kindnet-jjtgr               Created container: kindnet-cni
kube-system   15m                 Normal    Started                   Pod/kindnet-jjtgr               Started container kindnet-cni
kube-system   16m                 Normal    Scheduled                 Pod/kindnet-phcb4               Successfully assigned kube-system/kindnet-phcb4 to kind-control-plane
kube-system   16m                 Normal    Pulled                    Pod/kindnet-phcb4               Container image "docker.io/kindest/kindnetd:v20250512-df8de77b" already present on machine
kube-system   16m                 Normal    Created                   Pod/kindnet-phcb4               Created container: kindnet-cni
kube-system   16m                 Normal    Started                   Pod/kindnet-phcb4               Started container kindnet-cni
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kindnet               Created pod: kindnet-phcb4
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kindnet               Created pod: kindnet-gcnfs
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kindnet               Created pod: kindnet-c9qwt
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kindnet               Created pod: kindnet-jjtgr
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kindnet               Created pod: kindnet-6mlhj
kube-system   16m                 Normal    LeaderElection            Lease/kube-controller-manager   kind-control-plane_211d904b-24bd-4dfc-868e-a86b576a5033 became leader
kube-system   16m                 Normal    Scheduled                 Pod/kube-proxy-9jwdr            Successfully assigned kube-system/kube-proxy-9jwdr to node4
kube-system   16m                 Normal    Pulled                    Pod/kube-proxy-9jwdr            Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   15m                 Normal    Created                   Pod/kube-proxy-9jwdr            Created container: kube-proxy
kube-system   15m                 Normal    Started                   Pod/kube-proxy-9jwdr            Started container kube-proxy
kube-system   16m                 Normal    Scheduled                 Pod/kube-proxy-c6tm2            Successfully assigned kube-system/kube-proxy-c6tm2 to kind-control-plane
kube-system   16m                 Normal    Pulled                    Pod/kube-proxy-c6tm2            Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   16m                 Normal    Created                   Pod/kube-proxy-c6tm2            Created container: kube-proxy
kube-system   16m                 Normal    Started                   Pod/kube-proxy-c6tm2            Started container kube-proxy
kube-system   16m                 Normal    Scheduled                 Pod/kube-proxy-c8kpt            Successfully assigned kube-system/kube-proxy-c8kpt to node2
kube-system   16m                 Normal    Pulled                    Pod/kube-proxy-c8kpt            Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   16m                 Normal    Created                   Pod/kube-proxy-c8kpt            Created container: kube-proxy
kube-system   16m                 Normal    Started                   Pod/kube-proxy-c8kpt            Started container kube-proxy
kube-system   16m                 Normal    Scheduled                 Pod/kube-proxy-j6lhs            Successfully assigned kube-system/kube-proxy-j6lhs to node3
kube-system   16m                 Normal    Pulled                    Pod/kube-proxy-j6lhs            Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   15m                 Normal    Created                   Pod/kube-proxy-j6lhs            Created container: kube-proxy
kube-system   15m                 Normal    Started                   Pod/kube-proxy-j6lhs            Started container kube-proxy
kube-system   16m                 Normal    Scheduled                 Pod/kube-proxy-xtnlk            Successfully assigned kube-system/kube-proxy-xtnlk to node1
kube-system   16m                 Normal    Pulled                    Pod/kube-proxy-xtnlk            Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
kube-system   15m                 Normal    Created                   Pod/kube-proxy-xtnlk            Created container: kube-proxy
kube-system   15m                 Normal    Started                   Pod/kube-proxy-xtnlk            Started container kube-proxy
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kube-proxy            Created pod: kube-proxy-c6tm2
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kube-proxy            Created pod: kube-proxy-c8kpt
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kube-proxy            Created pod: kube-proxy-9jwdr
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kube-proxy            Created pod: kube-proxy-j6lhs
kube-system   16m                 Normal    SuccessfulCreate          DaemonSet/kube-proxy            Created pod: kube-proxy-xtnlk
kube-system   16m                 Warning   Unhealthy                 Pod/kube-scheduler-kind-control-plane   Readiness probe failed: HTTP probe failed with statuscode: 500
kube-system   16m                 Normal    LeaderElection            Lease/kube-scheduler                    kind-control-plane_3eeac50f-cab1-418c-b7e8-f1244c25613c became leader
local-path-storage   16m                 Warning   FailedScheduling          Pod/local-path-provisioner-7dc846544d-fm8tw   0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/not-ready: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
local-path-storage   15m                 Normal    Scheduled                 Pod/local-path-provisioner-7dc846544d-fm8tw   Successfully assigned local-path-storage/local-path-provisioner-7dc846544d-fm8tw to kind-control-plane
local-path-storage   15m                 Normal    Pulled                    Pod/local-path-provisioner-7dc846544d-fm8tw   Container image "docker.io/kindest/local-path-provisioner:v20250214-acbabc1a" already present on machine
local-path-storage   15m                 Normal    Created                   Pod/local-path-provisioner-7dc846544d-fm8tw   Created container: local-path-provisioner
local-path-storage   15m                 Normal    Started                   Pod/local-path-provisioner-7dc846544d-fm8tw   Started container local-path-provisioner
local-path-storage   16m                 Normal    SuccessfulCreate          ReplicaSet/local-path-provisioner-7dc846544d   Created pod: local-path-provisioner-7dc846544d-fm8tw
local-path-storage   16m                 Normal    ScalingReplicaSet         Deployment/local-path-provisioner              Scaled up replica set local-path-provisioner-7dc846544d from 0 to 1
kube-system          0s                  Normal    ScalingReplicaSet         Deployment/gpu-scheduler                       Scaled up replica set gpu-scheduler-77c89d4bfc from 0 to 1
kube-system          0s                  Normal    SuccessfulCreate          ReplicaSet/gpu-scheduler-77c89d4bfc            Created pod: gpu-scheduler-77c89d4bfc-8lwx7
kube-system          0s                  Normal    Scheduled                 Pod/gpu-scheduler-77c89d4bfc-8lwx7             Successfully assigned kube-system/gpu-scheduler-77c89d4bfc-8lwx7 to kind-control-plane
kube-system          0s                  Normal    Pulled                    Pod/gpu-scheduler-77c89d4bfc-8lwx7             Container image "gpu-scheduler:latest" already present on machine
kube-system          0s                  Normal    Created                   Pod/gpu-scheduler-77c89d4bfc-8lwx7             Created container: gpu-scheduler
kube-system          0s                  Normal    Started                   Pod/gpu-scheduler-77c89d4bfc-8lwx7             Started container gpu-scheduler
default              0s                  Normal    SuccessfulCreate          StatefulSet/gpu-scheduler-check                create Pod gpu-scheduler-check-0 in StatefulSet gpu-scheduler-check successful
default              0s                  Normal    Pulled                    Pod/gpu-scheduler-check-0                      Container image "gpu-scheduler-check:latest" already present on machine
default              0s                  Normal    Created                   Pod/gpu-scheduler-check-0                      Created container: gpu-scheduler-check
default              0s                  Normal    Started                   Pod/gpu-scheduler-check-0                      Started container gpu-scheduler-check
default              0s                  Normal    SuccessfulCreate          StatefulSet/gpu-scheduler-check                create Pod gpu-scheduler-check-1 in StatefulSet gpu-scheduler-check successful
default              0s                  Normal    Pulled                    Pod/gpu-scheduler-check-1                      Container image "gpu-scheduler-check:latest" already present on machine
default              0s                  Normal    Created                   Pod/gpu-scheduler-check-1                      Created container: gpu-scheduler-check
default              0s                  Normal    Started                   Pod/gpu-scheduler-check-1                      Started container gpu-scheduler-check
default              0s                  Normal    SuccessfulCreate          StatefulSet/gpu-scheduler-check                create Pod gpu-scheduler-check-2 in StatefulSet gpu-scheduler-check successful
default              0s                  Normal    Pulled                    Pod/gpu-scheduler-check-2                      Container image "gpu-scheduler-check:latest" already present on machine
default              0s                  Normal    Created                   Pod/gpu-scheduler-check-2                      Created container: gpu-scheduler-check
default              0s                  Normal    Started                   Pod/gpu-scheduler-check-2                      Started container gpu-scheduler-check
default              0s                  Normal    SuccessfulCreate          StatefulSet/gpu-scheduler-check                create Pod gpu-scheduler-check-3 in StatefulSet gpu-scheduler-check successful
default              0s                  Normal    Pulled                    Pod/gpu-scheduler-check-3                      Container image "gpu-scheduler-check:latest" already present on machine
default              0s                  Normal    Created                   Pod/gpu-scheduler-check-3                      Created container: gpu-scheduler-check
default              0s                  Normal    Started                   Pod/gpu-scheduler-check-3                      Started container gpu-scheduler-check
default              0s                  Normal    SuccessfulCreate          StatefulSet/gpu-scheduler-check                create Pod gpu-scheduler-check-4 in StatefulSet gpu-scheduler-check successful
default              0s                  Normal    Pulled                    Pod/gpu-scheduler-check-4                      Container image "gpu-scheduler-check:latest" already present on machine
default              0s                  Normal    Created                   Pod/gpu-scheduler-check-4                      Created container: gpu-scheduler-check
default              0s                  Normal    Started                   Pod/gpu-scheduler-check-4                      Started container gpu-scheduler-check
default              0s                  Normal    SuccessfulCreate          StatefulSet/gpu-scheduler-check                create Pod gpu-scheduler-check-5 in StatefulSet gpu-scheduler-check successful
```