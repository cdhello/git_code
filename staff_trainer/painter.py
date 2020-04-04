import pygame;
import os;
from grand_staff import *;
import random;

class CPainter():
    """
    Class to paint the GUI
    """

    STAFF_LINE_INTERVAL = 50;
    STAFF_LINE_LENGTH = STAFF_LINE_INTERVAL * 15;
    STAFF_LINE_WIDTH = 3;

    STAFF_X = STAFF_LINE_INTERVAL*3;
    STAFF_Y = STAFF_LINE_INTERVAL/2;

    LEDGER_LINE_LENGTH = STAFF_LINE_INTERVAL * 3 / 2;

    screen = pygame.display.set_mode(flags = pygame.FULLSCREEN);

    staff_position_Y = [];
    correct_pictures = [];
    incorrect_pictures = [];

    def __load_result_images(self, path):
        picture_W =  CPainter.STAFF_LINE_INTERVAL * 6

        images = []
        for i in os.listdir(path):
            try:
                _picture = pygame.image.load(path + i);
                (width, height) = _picture.get_size();
                picture = pygame.transform.smoothscale(_picture, (picture_W, height * picture_W / width));
                images.append(picture);
            except Exception as x:
                continue;
        return images

    def __init__(self):
        (w, h) = CPainter.screen.get_size();
        needing_h = CPainter.STAFF_LINE_INTERVAL * 24;
        if (h < needing_h):
            print("WARNING: Window size is (%d, %d), but a grand staff need a %d height for 24 spaces with line-interval %d."
                  %(w, h, needing_h, CPainter.STAFF_LINE_INTERVAL));

        for i in range(BASS_UNDER_LEDGER_SPACE_7 + 1):
            if i < BASS_UPPER_LEDGER_LINE_1:
                CPainter.staff_position_Y.append(CPainter.STAFF_Y + i * CPainter.STAFF_LINE_INTERVAL / 2);
            else:
                CPainter.staff_position_Y.append(CPainter.STAFF_Y + (i + 1) * CPainter.STAFF_LINE_INTERVAL / 2);

        whole_note = pygame.image.load("./res/notes/whole_note.png");
        CPainter.whole_note = pygame.transform.smoothscale(whole_note, (int(CPainter.STAFF_LINE_INTERVAL*1.2), int(CPainter.STAFF_LINE_INTERVAL*1.2)));

        half_note = pygame.image.load("./res/notes/half_note.png");
        (w,y) = (int(CPainter.STAFF_LINE_INTERVAL*3.8), int(CPainter.STAFF_LINE_INTERVAL*4));
        CPainter.half_note_low = pygame.transform.smoothscale(half_note, (w,y));
        CPainter.half_note_high = pygame.transform.flip(CPainter.half_note_low, False, True);

        quarter_note = pygame.image.load("./res/notes/quarter_note.png");
        (w,y) = (int(CPainter.STAFF_LINE_INTERVAL*3.8), int(CPainter.STAFF_LINE_INTERVAL*4));
        CPainter.quarter_note_low = pygame.transform.smoothscale(quarter_note, (w,y));
        CPainter.quarter_note_high = pygame.transform.flip(CPainter.quarter_note_low, False, True);

        eighth_note = pygame.image.load("./res/notes/eighth_note.png");
        (w,y) = (int(CPainter.STAFF_LINE_INTERVAL*3.8), int(CPainter.STAFF_LINE_INTERVAL*4));
        CPainter.eighth_note_low = pygame.transform.smoothscale(eighth_note, (w,y));
        CPainter.eighth_note_high = pygame.transform.flip(CPainter.eighth_note_low, False, True);

        CPainter.correct_pictures = self.__load_result_images("res/correct_pictures/");
        CPainter.incorrect_pictures = self.__load_result_images("res/incorrect_pictures/");

        CPainter.staff_surface = None;
        CPainter.asking_notes_surface = None;
        CPainter.answering_notes_surface = None;
        CPainter.result_surface = None;

        self.__paint_staff()
        self.__repaint()

    def __paint_staff(self):
        CPainter.staff_surface = pygame.Surface(CPainter.screen.get_size(), pygame.SRCALPHA, 32);

        CPainter.staff_surface.fill((204, 232, 207)); #Background

        black = (0,0,0);
        treble_lines = [TREBLE_LINE_5, TREBLE_LINE_4, TREBLE_LINE_3, TREBLE_LINE_2, TREBLE_LINE_1];
        bass_lines = [BASS_LINE_5, BASS_LINE_4, BASS_LINE_3, BASS_LINE_2, BASS_LINE_1];
        for i in treble_lines + bass_lines:
            Y = CPainter.staff_position_Y[i]
            pygame.draw.line(CPainter.staff_surface, black,
                             (CPainter.STAFF_X, Y), (CPainter.STAFF_X + CPainter.STAFF_LINE_LENGTH, Y),
                             CPainter.STAFF_LINE_WIDTH);

        pygame.draw.line(CPainter.staff_surface, black,
                         (CPainter.STAFF_X, CPainter.staff_position_Y[BASS_LINE_1]),
                         (CPainter.STAFF_X, CPainter.staff_position_Y[TREBLE_LINE_5]),
                         CPainter.STAFF_LINE_WIDTH * 2);
        pygame.draw.line(CPainter.staff_surface, black,
                         (CPainter.STAFF_X + CPainter.STAFF_LINE_LENGTH, CPainter.staff_position_Y[BASS_LINE_1]),
                         (CPainter.STAFF_X + CPainter.STAFF_LINE_LENGTH, CPainter.staff_position_Y[TREBLE_LINE_5]),
                         CPainter.STAFF_LINE_WIDTH * 2);

        _gclef = pygame.image.load("./res/gclef.png").convert_alpha();
        _fclef = pygame.image.load("./res/fclef.png").convert_alpha();
        gclef = pygame.transform.smoothscale(_gclef, (CPainter.STAFF_LINE_INTERVAL * 2, CPainter.STAFF_LINE_INTERVAL * 5));
        fclef = pygame.transform.smoothscale(_fclef, (CPainter.STAFF_LINE_INTERVAL * 2, CPainter.STAFF_LINE_INTERVAL * 5 / 2));

        clefx = CPainter.STAFF_X + CPainter.STAFF_LINE_INTERVAL/2;
        CPainter.staff_surface.blit(gclef, (clefx, CPainter.staff_position_Y[TREBLE_LINE_2] - gclef.get_size()[1]*2/3));
        CPainter.staff_surface.blit(fclef, (clefx, CPainter.staff_position_Y[BASS_LINE_4] - fclef.get_size()[1]/3));

    def __repaint(self):


        if CPainter.staff_surface:
            CPainter.screen.blit(CPainter.staff_surface, (0, 0)); #grand staff

        if CPainter.asking_notes_surface:
            CPainter.screen.blit(CPainter.asking_notes_surface, (0, 0));

        if CPainter.answering_notes_surface:
            CPainter.screen.blit(CPainter.answering_notes_surface, (0, 0));

        if CPainter.result_surface:
            CPainter.screen.blit(CPainter.result_surface,
                                 (CPainter.STAFF_LINE_LENGTH + CPainter.STAFF_LINE_INTERVAL * 5, CPainter.staff_position_Y[TREBLE_LINE_5]))

        pygame.display.update()

    def __paint_a_ledger(self, surface, pos, deltaX = 0):
        CPainter.LEDGER_LINE_LENGTH
        x1 = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX) - CPainter.LEDGER_LINE_LENGTH/2;
        x2 = x1 + CPainter.LEDGER_LINE_LENGTH;
        y = CPainter.staff_position_Y[pos];
        pygame.draw.line(surface, (0, 0, 0), (x1, y), (x2, y), CPainter.STAFF_LINE_WIDTH);

    def __paint_ledgers(self, surface, pos, deltaX = 0):
        if (pos == TREBLE_UNDER_LEDGER_LINE_1 or pos == BASS_UPPER_LEDGER_LINE_1):
            self.__paint_a_ledger(surface, pos, deltaX);

        i = TREBLE_UPPER_LEDGER_LINE_1
        while (i >= pos):
            self.__paint_a_ledger(surface, i, deltaX);
            i = i - 2

        i = BASS_UNDER_LEDGER_LINE_1;
        while (i <= pos):
            self.__paint_a_ledger(surface, i, deltaX);
            i = i + 2

    def __paint_a_whole_note(self, pos, deltaX = 0):
        (w, h) = CPainter.whole_note.get_size();
        x = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX) - w/2;
        y = CPainter.staff_position_Y[pos] - h/2;
        CPainter.asking_notes_surface.blit(CPainter.whole_note, (x,y));

    def __paint_a_half_note(self, pos, deltaX = 0):
        if (pos > TREBLE_LINE_3 and pos <= TREBLE_UNDER_LEDGER_LINE_1) or (pos > BASS_LINE_3):
            (w, h) = CPainter.half_note_low.get_size();
            x = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX) - w/2;
            y = int(CPainter.staff_position_Y[pos] - h * 0.841);

            CPainter.asking_notes_surface.blit(CPainter.half_note_low, (x,y));
        else:
            (w, h) = CPainter.half_note_high.get_size();
            x = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX) - w/2;
            y = int(CPainter.staff_position_Y[pos] - h * 0.15);
            CPainter.asking_notes_surface.blit(CPainter.half_note_high, (x,y));

    def __paint_a_quarter_note(self, pos, deltaX = 0):
        if (pos > TREBLE_LINE_3 and pos <= TREBLE_UNDER_LEDGER_LINE_1) or (pos > BASS_LINE_3):
            (w, h) = CPainter.quarter_note_low.get_size();
            x = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX) - w/2;
            y = int(CPainter.staff_position_Y[pos] - h * 0.841);

            CPainter.asking_notes_surface.blit(CPainter.quarter_note_low, (x,y));
        else:
            (w, h) = CPainter.quarter_note_high.get_size();
            x = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX) - w/2;
            y = int(CPainter.staff_position_Y[pos] - h * 0.15);
            CPainter.asking_notes_surface.blit(CPainter.quarter_note_high, (x,y));

    def __paint_a_eighth_note(self, pos, deltaX = 0):
         if (pos > TREBLE_LINE_3 and pos <= TREBLE_UNDER_LEDGER_LINE_1) or (pos > BASS_LINE_3):
             (w, h) = CPainter.eighth_note_low.get_size();
             x = CPainter.STAFF_LINE_INTERVAL * (7.45 + deltaX) - w/2;
             y = int(CPainter.staff_position_Y[pos] - h * 0.841);

             CPainter.asking_notes_surface.blit(CPainter.eighth_note_low, (x,y));
         else:
             (w, h) = CPainter.eighth_note_high.get_size();
             x = CPainter.STAFF_LINE_INTERVAL * (7.45 + deltaX) - w/2;
             y = int(CPainter.staff_position_Y[pos] - h * 0.15);
             CPainter.asking_notes_surface.blit(CPainter.eighth_note_high, (x,y));

    def update_asking_notes(self, asking_notes = []):
        CPainter.asking_notes_surface = pygame.Surface(CPainter.screen.get_size(), pygame.SRCALPHA, 32);
        for i in asking_notes:
            x = random.randint(0, 3);
            if x == 0:
                self.__paint_a_whole_note(i);
            elif x == 1:
                self.__paint_a_half_note(i);
            elif x == 2:
                self.__paint_a_quarter_note(i);
            elif x == 3:
                self.__paint_a_eighth_note(i);

            self.__paint_ledgers(CPainter.asking_notes_surface, i);
        self.__repaint()

    def __paint_ellipse(self, surface, pos, deltaX = 0):

        ellipse_width = int(CPainter.STAFF_LINE_INTERVAL * 1.2);
        x = CPainter.STAFF_LINE_INTERVAL * (7 + deltaX);
        left = x - ellipse_width/2
        y = CPainter.staff_position_Y[pos]
        top = y - CPainter.STAFF_LINE_INTERVAL/2

        #Rect(left, top, width, height) -> Rect
        note_rec = (left, top, ellipse_width, CPainter.STAFF_LINE_INTERVAL)
        pygame.draw.ellipse(surface, (0,200,0), note_rec, CPainter.STAFF_LINE_INTERVAL/2)

    def update_answering_notes(self, answering_notes = []):
        CPainter.answering_notes_surface = pygame.Surface(CPainter.screen.get_size(), pygame.SRCALPHA, 32);

        for i in answering_notes:
            self.__paint_ellipse(CPainter.answering_notes_surface, i, 6);
            self.__paint_ledgers(CPainter.answering_notes_surface, i, 6);

        self.__repaint()

    def update_result(self, result = None):
        if result == True:
            CPainter.result_surface = CPainter.correct_pictures[random.randint(0, len(CPainter.correct_pictures)-1)];
        elif result == False:
            CPainter.result_surface = CPainter.incorrect_pictures[random.randint(0, len(CPainter.incorrect_pictures)-1)];
        else:
            CPainter.result_surface = None

        self.__repaint()

if __name__ == '__main__':
    import time;
    x = CPainter();

    x.update_asking_notes();

    from pygame.locals import *;
    import sys;
    pygame.fastevent.init();
    while True:
    #for event in pygame.event.get():
        for event in pygame.fastevent.get():
            if event.type != MOUSEMOTION:
                print "fastevent:",event;
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

