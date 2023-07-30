#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""This module displays plex stats on the 2in13 display"""
import logging
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import epd2in13_V3
import plex_tautulli_client as plex_client

FONT_DIR = Path(__file__).parent.parent / "resources/fonts"
logging.basicConfig(level=logging.INFO)

FONT22 = ImageFont.truetype(str(FONT_DIR / "Font.ttc"), 22)
FONT18 = ImageFont.truetype(str(FONT_DIR / "Font.ttc"), 18)
FONT14 = ImageFont.truetype(str(FONT_DIR / "Font.ttc"), 14)
FONT11 = ImageFont.truetype(str(FONT_DIR / "Font.ttc"), 11)

EPD = epd2in13_V3.EPD()


def title_format(title) -> str:
    """Formats title so it fits on screen"""
    limit = 24
    return f"{title[:limit]}..." if len(title) > limit + 3 else title


def format_media_title(session: dict) -> str:
    """Format title based on media type."""
    if session["media_type"] == "episode":
        title = title_format(session["grandparent_title"])
        season = session["parent_media_index"]
        episode = session["media_index"]
        return f"{title} S{season}E{episode}"
    return title_format(session["title"])


def init_display():
    logging.info("Running Plex Display")
    EPD.init()
    EPD.Clear(0xFF)
    logging.info("Clearing display...")
    image = Image.new("1", (EPD.height, EPD.width), 255)
    return image, ImageDraw.Draw(image)


def draw_text(plex):
    image, draw = init_display()
    draw.rectangle([(0, 0), (242, 44)], outline=0)

    if plex.check_if_alive():
        draw.text((5, 5), "Plex Online", font=FONT22, fill=0)
        status = plex.get_activity()
        draw_status_info(draw, status)
        check_updates(draw, plex)
    else:
        draw.text((5, 5), "Plex Offline", font=FONT22, fill=0)

    last_checked = f"Last checked - {time.strftime('%H:%M')}"
    draw.text((140, 30), last_checked, font=FONT11, fill=0)

    image = image.rotate(180)  # rotate
    EPD.display(EPD.getbuffer(image))


def draw_status_info(draw, status):
    if status:
        draw.text((140, 4), f"Streams: {status[0]}", font=FONT14, fill=0)
        draw.text((140, 18), f"{status[1]}kbs", font=FONT14, fill=0)
        loc_y = 44
        for session in status[2]:
            username = session["username"]
            progress = session["progress_percent"]
            title = format_media_title(session)
            draw.text(
                (5, loc_y),
                f"{username} - {title} ({progress}%)",
                font=FONT11,
                fill=0,
            )
            loc_y += 12
    else:
        draw.text((10, 44), "Error", font=FONT22, fill=0)


def check_updates(draw, plex):
    if plex.check_for_update():
        draw.text((5, 26), "Update Available", font=FONT14, fill=0)
    else:
        draw.text((5, 26), "Up to date", font=FONT14, fill=0)


def main():
    """Main Method, updates the display stats"""
    plex = plex_client.Plex()
    draw_text(plex)


if __name__ == "__main__":
    main()
