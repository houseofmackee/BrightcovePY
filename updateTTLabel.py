#!/usr/bin/env python3
from mackee import main, get_cms

#===========================================
# callback to update text track labels to
# match the language
#===========================================
def update_tt_label(video: dict):
    """
    This will update a text track's label to be the same as the language.
    """
    # try to get all text tracks
    if tts := video.get('text_tracks'):
        # go through all tracks
        for track in tts:
            # change the setting
            track['label'] = track['srclang']

        # get the video ID
        video_id = video.get('id')
        # create the JSON body
        json_body = { 'text_tracks': tts }
        # make the PATCH call
        r = get_cms().UpdateVideo(video_id=video_id, json_body=json_body)
        # check if all went well
        if r.status_code in [200,202]:
            print(f'Updated track labels for video ID {video_id} with status {r.status_code}.')
        # otherwise report the error
        else:
            print(f'Error code {r.status_code} updating track labels for video ID {video_id}:')
            print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(update_tt_label)
