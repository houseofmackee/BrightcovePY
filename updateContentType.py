"""
Example script to update content type for videos in an account
"""
from mackee import main, get_oauth
from brightcove.Audience import Audience

# global Audience API instance
aapi : Audience = None

#===========================================
# callback to set content type for videos
#===========================================
def update_content_type(video: dict):
    """
    Updates content type for a video.
    """
    global aapi

    # get an Audience API instance in case we don't have one yet
    if not aapi:
        aapi = Audience(get_oauth())

    # get video ID and specify content type
    video_id = video.get('id')
    content_type = 'my-type-here'

    # make API call
    response = aapi.SetContentType(video_id=video_id, content_type=content_type)

    # check if we have a scuccess response
    if response.status_code in [200,202]:
        print(f'Updated content type for video ID {video_id} with status {response.status_code}.')
    else:
        print(f'Error code {response.status_code} updating content type for video ID {video_id}:')
        print(response.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
    main(update_content_type)
