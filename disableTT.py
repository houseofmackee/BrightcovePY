"""
Script to disable "default" text tracks in videos.
"""
from mackee import main, get_cms

#===========================================
# callback to disable all default tracks
#===========================================
def disable_tt(video: dict):
    """
    This will find text tracks with default tracks and disable those defaults.
    """
    # try to get all text tracks
    if tts := video.get('text_tracks'):
        # flag to signal we found and changed default tracks
        got_hit = False
        # go through all tracks
        for track in tts:
            #check if it's a default track
            if track.get('default'):
                # change the setting
                track['default'] = False
                # set the flag so we know we found one
                got_hit = True

        # check if we found and changed at least one
        if got_hit:
            # get the video ID
            video_id = video.get('id')
            # create the JSON body
            json_body = { 'text_tracks': tts }
            # make the PATCH call
            r = get_cms().UpdateVideo(video_id=video_id, json_body=json_body)
            # check if all went well
            if r.status_code in [200,202]:
                print(f'Disabled default track(s) for video ID {video_id} with status {r.status_code}.')
            # otherwise report the error
            else:
                print(f'Error code {r.status_code} disabling default track(s) for video ID {video_id}:')
                print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(disable_tt)
