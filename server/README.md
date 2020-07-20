## About

Demo of digital native -- Robotic arm

To be added.

## Usage

``` BASH
################# ui test ##################
docker rm arm_demo -f
docker run -d --name arm_demo -v `pwd`/ui/:/usr/share/nginx/html -p 8090:80 nginx:alpine
# update ui
docker restart arm_demo


################## deploy ##################
# build ui
docker build -f ./deploy/Dockerfile-ui -t arm-ui:v3 .
# build image for docker run
docker build -f ./deploy/Dockerfile-docker -t arm-server:v5 .
# build image for k8s
docker build -f ./deploy/Dockerfile-k8s -t arm-server:v5.1 .
# build image for fileUploader
docker build -f deploy/Dockerfile-fileUploader -t file-uploader:1.1 .
# rmove the limit of k8s port (run on k8s master)
sed -i '/- kube-apiserver/a\    - --service-node-port-range=8000-65535' /etc/kubernetes/manifests/kube-apiserver.yaml
# restart kube-apiserver
systemctl restart kubelet

################## tools ###################
# get tcp
sudo ss -lntpd
sudo netstat -tnlp
# get process
ps -aux
# for test
# wscat -c ws://10.164.17.14:8181
docker run -it --rm --device /dev/gpiomem -p 8947:8947 -p 18181:8181 --entrypoint bash arm-server:v5
docker run --device /dev/gpiomem -p 8947:8947 -p 18181:8181 -d arm-server:v5
docker run -it -d -p 8182:8080 -v `pwd`/server/fileUploader.py:/home/pi/fileUploader/fileUploader.py file-uploader:1.1
docker run -it -d -p 8182:8080 -v `pwd`/server/fileUploader.py:/home/pi/fileUploader/fileUploader.py -v `pwd`/images:/home/pi/fileUploader/upload file-uploader:1.1
docker run -it -d -p 8183:8080 -v `pwd`/server/getPos.py:/home/pi/fileUploader/fileUploader.py -v `pwd`/images:/home/pi/fileUploader/upload file-uploader:1.1
```