import os
from datetime import datetime
import tweepy
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

# get environment variables for Twitter API
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")


def twitter_api_authenticate():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
    except Exception as error:
        print(
            f"\n[ SimJowBot ] An error occurred while attempting to authenticate with the twitter API. Reason:\n{error}"
        )
        return None
    else:
        return api


def get_tweet(twitterApi, tweetId):
    userName = None
    tweetText = None

    if twitterApi:
        try:
            status = twitterApi.get_status(id=tweetId)
        except Exception as error:
            print(
                f"\n[ SimJowBot ] An error occurred while attempting to get the twitter status with id={tweetId}. Reason:\n{error}"
            )
        else:
            userName = status.user.name
            tweetText = status.text

    return userName, tweetText


def post_tweet(twitterApi, tweetText):
    success = False

    if twitterApi:
        try:
            twitterApi.update_status(status=tweetText)
        except Exception as error:
            print(
                f"\n[ SimJowBot ] An error occurred while attempting to update the twitter status. Reason:\n{error}"
            )
        else:
            success = True

    return success


class SimJowStream(tweepy.Stream):
    def __init__(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        super().__init__(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        self.twitterApi = twitter_api_authenticate()
        self.myUser = self.twitterApi.get_user(screen_name="SimJow")

    # when a new tweet is posted on Twitter with your filtered specifications
    def on_status(self, status):

        # If the found tweet is not a reply to another tweet
        if self.is_not_a_reply(status):
            # If the user is not myself
            if status.user.screen_name != self.myUser.screen_name:

                print(
                    f"\n[ SimJowBot ] Found a matching tweet https://twitter.com/{status.user.screen_name}/status/{status.id} "
                )
                # Retweet the found tweet (status)
                self.retweet(status)
                # Like the found tweet (status)
                self.like(status)

    def retweet(self, status):
        try:
            # Retweet the tweet
            self.twitterApi.retweet(status.id)
        # Some basic error handling. Will print out why retweet failed, into your terminal.
        except Exception as error:
            print(f"[ SimJowBot ] ERROR: Retweet was not successful. Reason:\n{error}")
        else:
            print(f"[ SimJowBot ] Retweeted successfully.")

    def like(self, status):
        try:
            # Like the tweet
            self.twitterApi.create_favorite(status.id)
        # Some basic error handling. Will print out why retweet failed, into your terminal.
        except Exception as error:
            print(f"[ SimJowBot ] ERROR: Favorite was not successful. Reason:\n{error}")
        else:
            print(f"[ SimJowBot ] Favorited successfully.")

    def is_not_a_reply(self, status):
        if status.in_reply_to_status_id == None:
            return True
        else:
            return False


if __name__ == "__main__":

    keywordsList = [
        "ترانزیستور",
        "ماسفت",
        "MOSFET",
        "دیود",
        "خازن",
        "بورد الکترونیکی",
        "مدار الکترونیکی",
        "برد الکترونیکی",
        "قطعه الکترونیکی",
        "رباتیک",
        "مکاترونیک",
        "امبدد",
        "سیستم های نهفته",
        "سیستم های توکار",
        "سیستم‌های نهفته",
        "سیستم‌های توکار",
        "Arduino",
        "آردوینو",
        "Raspberry Pi",
        "Orange Pi",
        "BeagleBone",
        "Zybo",
        "ZC706",
        "Digilent",
        "دیجیلنت",
        "رزبری پای",
        "رزپری پای",
        "رسپری پای",
        "رزبری‌پای",
        "رزپری‌پای",
        "رسپری‌پای",
        "VHDL",
        "HDL",
        "Verilog",
        "توصیف سخت افزار",
        "توصیف سخت‌افزار",
        "FPGA",
        "میکروکنترلر",
        "میکروپروسسور",
        "ریزپردازنده",
        "Microcontroller",
        "Microprocessor",
        "Ryzen",
        "Nvidia",
        "انویدیا",
        "GeForce",
        "جیفورس",
        "جی‌فورس",
        "گرافیک RTX",
        "گرافیک GTX",
        "گرافیکی RTX",
        "گرافیکی GTX",
        "Embedded",
        "Embedded Linux",
        "UBoot",
        "U-Boot",
        "Yocto",
        "یوکتو",
        "یاکتو",
        "Electronics",
        "Robotics",
        "Mechatronics",
        "Altium",
        "Altium Designer",
        "PCB",
        "PCB Design",
        "آلتیوم",
        "آلتیوم دیزاینر",
        "Vivado",
        "Xilinx",
        "زایلینکس",
        "Altera",
        "Zynq",
        "اف‌پی‌جی‌ای",
        "پردازنده",
        "CPU",
        "GPU",
        "ASIC",
        "سیسوگ",
        "اسنپدراگون",
        "تراشه",
        "کوالکام",
        "Qualcomm",
        "Snapdragon",
        "TSMC",
        "Chipset",
        "پورت USB",
        "HDMI",
        "PCI",
        "پی‌سی‌آی",
        "UART",
        "USART",
        "پورت سریال",
        "Core i3",
        "Core i5",
        "Core i7",
        "Core i9",
        "M1 اپل",
        "M1 پردازنده",
        "M1 Max",
        "M1 Pro",
        "تنسور گوگل",
        "Google Tensor",
        "گوکل Tensor",
        "پردازنده آرم",
        "معماری آرم",
        "پردازنده ARM",
        "معماری ARM",
        "PowerPC",
        "x86",
        "x86_64",
        "DDR3",
        "DDR4",
        "DRAM",
        "SRAM",
        "Mouser",
        "Digikey",
        "دیجی‌کی",
        "دیجیکی",
    ]

    hashtagsList = [
        "الکترونیک",
        "RaspberryPi",
        "OrangePi",
        "آی_سی",
        "رزبری_پای",
        "رزپری_پای",
        "رسپری_پای",
        "اف_پی_جی_ای",
        "آلتیوم_دیزاینر",
        "PCBDesign",
        "AltiumDesigner",
        "EmbeddedLinux",
    ]

    mentionsList = [
        "@SimJow",
    ]

    # Add hashtags to track list with # added at the beginning of each item
    trackList = []
    for i in range(len(hashtagsList)):
        tmpStr = "#" + hashtagsList.pop()
        trackList.append(tmpStr)

    # Add keywords to track list
    trackList.extend(keywordsList)

    # Add mentions to track list
    trackList.extend(mentionsList)

    # create a tweepy Stream object for real time filtering of latest posted tweets
    stream = SimJowStream(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    stream.filter(track=trackList, languages=["fa"])
