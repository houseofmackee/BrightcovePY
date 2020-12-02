#!/usr/bin/env python3
from mackee import main, GetCMS, aspect_ratio

#=============================================
# callback to find the aspect ratio of videos
#=============================================
def find_aspect_ratios(video):
	video_id = str(video.get('id'))
	delivery_type = video.get('delivery_type')
	source_w, source_h, response = None, None, None

	if delivery_type == 'static_origin':
		response = GetCMS().GetRenditionList(video_id=video_id)
	elif delivery_type == 'dynamic_origin':
		response = GetCMS().GetDynamicRenditions(video_id=video_id)
	else:
		print(f'No video dimensions found for video ID {video_id} (delivery type: {delivery_type}).')
		return

	if response.status_code in GetCMS().success_responses:
		renditions = response.json()
		for rendition in renditions:
			if rendition.get('media_type') == 'video' or rendition.get('audio_only') == False:
				source_w = rendition.get('frame_width')
				source_h = rendition.get('frame_height')
				break

		if source_h and source_w:
			x,y = aspect_ratio(source_w, source_h)
			print(f'{video_id}: {x}x{y}')
		else:
			print(f'No video renditions found for video ID {video_id}.')

	else:
		print(f'Could not get renditions for video ID {video_id}.')

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(find_aspect_ratios)
