@echo on
bash -c "docker run --rm -it -w /home/user --mount type=bind,source=/mnt/c,target=/c schmools/graph-tool"
