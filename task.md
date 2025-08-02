Write a Kubernetes scheduler named `gpu-scheduler` in Python or Go that will place pods and sets environment variable `CUDA_VISIBLE_DEVICES` according to the annotation:

```yaml
gpu-scheduling-map: |
0=node1:0,1
1=node2:2
2=node3:0,1,2
3=node4:3
4=node4:3
```

```ruby
0=node1:0,1
    0 is the pod index, node1 is the node name, 0,1 is the value for the environment variable CUDA_VISIBLE_DEVICES.

1=node2:2
    1 is the pod index, node2 is the node name, 2 is the value for the environment variable CUDA_VISIBLE_DEVICES.
etc.
```
The result of the task should be a repository containing:
1. The GPU scheduler code
2. A Dockerfile for the gpu-scheduler
3. A Dockerfile for a test service called gpu-scheduler-check, which will use the gpu-scheduler. Upon startup, the service should log the node name and the value of the CUDA_VISIBLE_DEVICES environment variable in an infinite loop.

Next, you need to create a Kubernetes cluster (KinD, microk8s, etc.) with 1 master and 4 nodes named node1, ..., node4 and install the `gpu-scheduler` and `gpu-scheduler-check`

Include in the repository the output of the command `kubectl get pod -owide -A` and the logs of pods located on node3 and node4.
