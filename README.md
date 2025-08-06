
## Custom k8s scheduler in python
### 1. Task explained in [task.md](./task.md)
### 2. Resulting logs and screenshots shown [here](./output/README.md)

### 3. Steps
1. **Spin up Ubuntu VM** in Proxmox (QEMU, cloud-init, etc). VM size **tested** with kind:  4CPU, 8 GB RAM, 30Gb.  
    *Note: you can install docker/minikube locally on your laptop*
2. **Install Docker, Kind, kubectl**
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh

    sudo usermod -aG docker ubuntu
    # logout / login

    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind

    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl

    # Create/delete cluster to test that it works
    kind create cluster 
    kind delete cluster   
    ```
3. **Copy repo to VM**
    ```bash
    rsync -avz ./ ubuntu@your_vm_ip:/home/ubuntu/k8s-scheduler
    # or use git clone
    ```
4. **Start Kind cluster with 5 nodes**:
    ```bash
    # inside repo_dir
    kind create cluster --config kind-config.yaml
    
    kubectl cluster-info --context kind-kind

    # check status, before doing anything else
    kubectl get nodes
    kubectl get pods -owide -A
    ```
5. **Build Docker images**:
    ```bash
    docker build -t gpu-scheduler:latest ./gpu-scheduler
    docker build -t gpu-scheduler-check:latest ./gpu-scheduler-check
    ```
6. **Load images into Kind nodes**:  
    
    ```bash
    kind load docker-image gpu-scheduler:latest
    kind load docker-image gpu-scheduler-check:latest
    ```

7. **Apply manifests**:
    ```bash
    # kubectl apply -f manifests/rbac.yaml
    # rbac is broken, use k8sadmin meanwhile
    kubectl create serviceaccount k8sadmin -n kube-system; kubectl create clusterrolebinding k8sadmin-binding --clusterrole=cluster-admin --serviceaccount=kube-system:k8sadmin

    kubectl apply -f manifests/gpu-scheduler.yaml
    kubectl apply -f manifests/gpu-scheduler-check.yaml
    ```

8. **Verify deployment**:
    ```bash
    # better run in 4 different windows
    # or use tmux
    kubectl get pods -owide -w -A
    kubectl events -w -A
    kubectl logs -f deployments/gpu-scheduler -n kube-system
    kubectl logs statefulsets/gpu-scheduler-check --all-pods=true -f --timestamps
    ```


### 4. Notes
#### 4.1. IF you get "Failed to create inotify object: Too many open files"
- [link](https://github.com/spectrocloud/cluster-api/blob/master/docs/book/src/user/troubleshooting.md#cluster-api-with-docker----too-many-open-files)
    ```bash
    sudo sysctl fs.inotify.max_user_instances=8192
    ```

#### 4.2. TODO: Debug RBAC, see spoiler
<details><summary>Spoiler</summary>

```bash
kubectl auth can-i --list  --as=system:serviceaccount:default:gpu-scheduler
Resources                                       Non-Resource URLs                      Resource Names   Verbs
events                                          []                                     []               [create update patch]
pods/binding                                    []                                     []               [create]
selfsubjectreviews.authentication.k8s.io        []                                     []               [create]
selfsubjectaccessreviews.authorization.k8s.io   []                                     []               [create]
selfsubjectrulesreviews.authorization.k8s.io    []                                     []               [create]
pods                                            []                                     []               [get list watch update patch]
nodes                                           []                                     []               [get list watch]
                                                [/.well-known/openid-configuration/]   []               [get]
                                                [/.well-known/openid-configuration]    []               [get]
                                                [/api/*]                               []               [get]
                                                [/api]                                 []               [get]
                                                [/apis/*]                              []               [get]
                                                [/apis]                                []               [get]
                                                [/healthz]                             []               [get]
                                                [/healthz]                             []               [get]
                                                [/livez]                               []               [get]
                                                [/livez]                               []               [get]
                                                [/openapi/*]                           []               [get]
                                                [/openapi]                             []               [get]
                                                [/openid/v1/jwks/]                     []               [get]
                                                [/openid/v1/jwks]                      []               [get]
                                                [/readyz]                              []               [get]
                                                [/readyz]                              []               [get]
                                                [/version/]                            []               [get]
                                                [/version/]                            []               [get]
                                                [/version]                             []               [get]
                                                [/version]                             []               [get]
pods/status                                     []                                     []               [update]

kubectl describe clusterrole gpu-scheduler
Name:         gpu-scheduler
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources     Non-Resource URLs  Resource Names  Verbs
  ---------     -----------------  --------------  -----
  events        []                 []              [create update patch]
  pods/binding  []                 []              [create]
  pods          []                 []              [get list watch update patch]
  nodes         []                 []              [get list watch]
  pods/status   []                 []              [update]


kubectl auth can-i bind pods --as=system:serviceaccount:default:gpu-scheduler
no
```

</details>



### 5. Materials used
- [access-cluster-api](https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/)
- [access-api-from-pod](https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/)
- [in_cluster_config.py](https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py)
- [medium guide](https://sebgoa.medium.com/kubernetes-scheduling-in-python-3588f4928b13)
- [advanced scheduling (k8s blog)](https://kubernetes.io/blog/2017/03/advanced-scheduling-in-kubernetes/)
- [11-different-schedulers](https://overcast.blog/11-awesome-kubernetes-custom-schedulers-you-should-use-a29e86c82838)
- [Random Kubernetes scheduler in Golang](https://github.com/banzaicloud/random-scheduler)
- [kubernetes-python-client](https://www.velotio.com/engineering-blog/kubernetes-python-client)
- https://martinheinz.dev/blog/73
- [kind-load-docker-image](https://iximiuz.com/en/posts/kubernetes-kind-load-docker-image/)
- https://kubernetes.io/docs/tasks/extend-kubernetes/configure-multiple-schedulers/
- https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#create_namespaced_binding
- https://github.com/kubernetes-client/python/issues/547#issuecomment-440528154
- https://github.com/kubernetes/kubernetes/issues/19367
- https://stackoverflow.com/a/56436626
- https://spacelift.io/blog/kubectl-patch-command