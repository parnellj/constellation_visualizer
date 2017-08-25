import urllib2
import os
import sys
import pandas as pd
import pygame
import numpy as np
import pickle
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

PX_WIDTH, PX_HEIGHT = 1600, 900
RA_MIN, RA_MAX, RA_RNG = 0., 24., 24.
DE_MIN, DE_MAX, DE_RNG = -90., 90., 180.

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((PX_WIDTH, PX_HEIGHT))
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 12)

def make_bboxes(df):
    boxes = []
    for i, row in df.iterrows():
        start = coords_to_px(row['ra_low_frac'], row['dec_low_frac'])
        end = coords_to_px(row['ra_high_frac'], row['dec_high_frac'])
        mid = coords_to_px(row['ra_mid_frac'], row['dec_mid_frac'])
        textsurface = myfont.render(row['constellation'], False, (0, 0, 0))
        text_rect = textsurface.get_rect()
        mid = (mid[0] - (text_rect.width / 2), mid[1])
        text_rect = text_rect.move(-(text_rect.width / 2), 0)
        text_rect = text_rect.move(mid)
        boxes.append({'name':row['constellation'], 'txt': textsurface,
                      'text_rect': text_rect,
                      'midpoint': mid, 'rect': points_to_rect(start, end)})
    return boxes

def points_to_rect(a, b):
    diff = np.array(b) - np.array(a)
    return pygame.Rect(a, diff)

def coords_to_px(ra, de):

    x = int(((ra - RA_MIN) / RA_RNG) * PX_WIDTH)
    y = abs(PX_HEIGHT - (((de - DE_MIN) / DE_RNG) * PX_HEIGHT))
    if x < 0:
        print str(x)
    return x, y

def download_constellations(abbreviation):
    if os.path.exists(os.sep.join(['.', 'outputs', 'GIFs', abbreviation + '.gif'])):
        return None
    with open(os.sep.join(['.', 'GIFs', abbreviation + '.gif']), 'wb') as gif:
        print os.sep.join(['.', 'GIFs', abbreviation + '.gif'])
        print 'https://www.iau.org/static/public/constellations/gif/' + abbreviation + '.gif'
        response = urllib2.urlopen('https://www.iau.org/static/public/constellations/gif/' + abbreviation + '.gif')
        gif.write(response.read())

def download_points(abbreviation):
    points = []
    if os.path.exists(os.sep.join(['.', 'TXTs', abbreviation + '.txt'])):
        return None

    with open(os.sep.join(['.', 'outputs', 'TXTs', abbreviation + '.txt']), 'w') as txt:
        response = urllib2.urlopen('https://www.iau.org/static/public/constellations/txt/' + abbreviation.lower() + '.txt')
        txt.write(response.read())

        for line in response:
            if line == '\n': continue
            ra, dec, _ = [el.strip() for el in line.split('|')]
            ra = ra.split(' ')
            ra = float(ra[0]) + (float(ra[1]) / 60) + (float(ra[2]) / 3600)
            points.append([ra, float(dec)])
    return points

def read_points(file):
    points = []
    with open(file, 'r') as txt:
        for line in txt:
            if line in ['\r\n', '\n']: continue
            ra, dec, _ = [el.strip() for el in line.split('|')]
            ra = ra.split(' ')
            ra = float(ra[0]) + (float(ra[1]) / 60) + (float(ra[2]) / 3600)
            points.append([ra, float(dec)])
    return points

def main():
    pass

class Core(object):
    def __init__(self, surface, name, df):
        pygame.display.set_caption(name)
        self.df = df
        self.screen = surface
        self.clock = pygame.time.Clock()
        self.cur_gen = []
        self.initialize()
        self.bb = make_bboxes(constellation_df)
        self.img = None

    def dispatch(self, event):
        """
        Dispatcher that emits pygame commands based on input events.
        :param event: A PyGame event.
        :type event: event
        :return: None
        :rtype: NoneType
        """
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.initialize()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            print p
            for b in self.bb:
                if b['text_rect'].collidepoint(p):
                    match = self.df.loc[self.df['constellation'] == b['name']]['abbreviation_upper'].values[0]
                    self.img = pygame.image.load(os.sep.join(['.', 'GIFs', match + '.gif']))



            pass

    def run(self):
        while True:
            for event in pygame.event.get():
                self.dispatch(event)
            self.screen.fill([0xFF, 0xFF, 0xFF])
            for b in self.bb:
                # textsurface = myfont.render(b['name'], False, (0, 0, 0))
                # w = textsurface.get_rect().width
                screen.blit(b['txt'], b['midpoint'])

            tracings = []
            for i, row in constellation_df.iterrows():
                pts = row['points_px']
                if not pts: continue
                for a, b in zip(row['points_px'], row['points_px'][1:]):
                    if abs(a[0] - b[0]) > (20 / RA_MAX) * PX_WIDTH: continue
                    pygame.draw.line(self.screen, (0x80, 0x0, 0x0), a, b)
            if self.img:
                screen.blit(self.img,(0,0))
            pygame.display.flip()

    def initialize(self):
        pass

if __name__ == '__main__':
    constellation_df = pd.read_csv(os.sep.join('.', 'inputs', 'constellation_data.csv')
    constellation_df['points'] = object
    constellation_df['points_px'] = object
    for i, row in constellation_df.iterrows():
        try:
            download_constellations(row['abbreviation_upper'])
        except:
            continue
        print 'downloaded ' + row['abbreviation']
    for i, row in constellation_df.iterrows():
        p = read_points(os.sep.join(['.', 'outputs', 'TXTs', row['abbreviation_upper'] + '.txt']))
        constellation_df.set_value(i, 'points', p)
        constellation_df.set_value(i, 'points_px', [coords_to_px(ra, de) for ra, de in p])

    main = Core(screen, 'Node', constellation_df)
    main.run()
    print 'done'
