# lauch worker.py in background
nohup bash -c "lt -h https://tunnel.stableai.club --port 80 -s $INSTANCE_ID  &" && sleep 1
python instanceBeacon.py
python worker.py &
# launch the main process
flask run --host=0.0.0.0 -p 80