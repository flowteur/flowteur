# get MASTODON_SECRET from env and write to file token.secret
echo $MASTODON_SECRET > token.secret

# loop forever and sleep 1  minute
while true
do
    # run insta_life.py
    python3 insta_life.py
    # sleep 1 minute
    sleep 60
done
