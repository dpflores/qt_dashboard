try:
    from o2x5xx import ImageClient
except ModuleNotFoundError:
    from o2x5xx.device.image_client import ImageClient
    
import matplotlib.pyplot as plt

imageWidth = 1280
imageHeight = 960

class ImageStreamer():
    def __init__(self, address='192.168.0.5', port=50010):
        self.image_client = ImageClient(address, port)
    
    def get_frame(self):
        self.image_client.read_next_frames()
        return self.image_client.frames[0]


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     address = sys.argv[1]
    # else:
    #     address = '192.168.0.5'

    # # create grabber
    # image_client = ImageClient(address, 50010)

    # # create figures
    # figs = [image_client.make_figure(i) for i in range(image_client.number_images)]

    # def update_fig(*args):
    #     if args[3]:
    #         image_client.read_next_frames()
    #     image = args[2]
    #     idx = args[1]
    #     image.set_array(image_client.frames[idx])

    #     return image,


    # # List of animation objects for tracking
    # anim = []

    # # Animate the figures
    # flag = True

    # for i, frame_figure in enumerate(figs):
    #     fig, ax, im = frame_figure
    #     anim.append(animation.FuncAnimation(fig, update_fig, interval=10, blit=True, fargs=[i, im, flag, ]))

    #     # With more than 3 images, the image synchronization is poor
    #     if image_client.number_images >= 3:
    #         flag = False

    # plt.tight_layout()[[[]]]
    # plt.show()
    streamer = ImageStreamer()
    while True:
        frame = streamer.get_frame()
        
        print(frame)



