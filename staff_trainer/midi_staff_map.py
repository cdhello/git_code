import midi;
import grand_staff;

class CMidi_staff:

    def pos_2_midi(self, pos):
        if pos in self.__pos_2_midi:
            return self.__pos_2_midi[pos];
        else:
            return -1;

    def midi_2_pos(self, midi_note):
        if midi_note in self.__midi_2_pos:
            return self.__midi_2_pos[midi_note];
        else:
            return [];

    def doremi_2_pos(self, note):
        if note in self.__doremi_2_pos:
            return self.__doremi_2_pos[note];
        else:
            return [];

    def __init__(self):
        #c Major, others need give offset on midi key
        self.__pos_2_midi = {
            grand_staff.TREBLE_UPPER_LEDGER_SPACE_6    :midi.C7,
            grand_staff.TREBLE_UPPER_LEDGER_LINE_5     :midi.B6,
            grand_staff.TREBLE_UPPER_LEDGER_SPACE_5    :midi.A6,
            grand_staff.TREBLE_UPPER_LEDGER_LINE_4     :midi.G6,
            grand_staff.TREBLE_UPPER_LEDGER_SPACE_4    :midi.F6,
            grand_staff.TREBLE_UPPER_LEDGER_LINE_3     :midi.E6,
            grand_staff.TREBLE_UPPER_LEDGER_SPACE_3    :midi.D6,
            grand_staff.TREBLE_UPPER_LEDGER_LINE_2     :midi.C6,
            grand_staff.TREBLE_UPPER_LEDGER_SPACE_2    :midi.B5,
            grand_staff.TREBLE_UPPER_LEDGER_LINE_1     :midi.A5,
            grand_staff.TREBLE_UPPER_LEDGER_SPACE_1    :midi.G5,
            grand_staff.TREBLE_LINE_5                  :midi.F5,
            grand_staff.TREBLE_SPACE_4                 :midi.E5,
            grand_staff.TREBLE_LINE_4                  :midi.D5,
            grand_staff.TREBLE_SPACE_3                 :midi.C5,
            grand_staff.TREBLE_LINE_3                  :midi.B4,
            grand_staff.TREBLE_SPACE_2                 :midi.A4,
            grand_staff.TREBLE_LINE_2                  :midi.G4,
            grand_staff.TREBLE_SPACE_1                 :midi.F4,
            grand_staff.TREBLE_LINE_1                  :midi.E4,
            grand_staff.TREBLE_UNDER_LEDGER_SPACE_1    :midi.D4,
            grand_staff.TREBLE_UNDER_LEDGER_LINE_1     :midi.C4,
            grand_staff.BASS_UPPER_LEDGER_LINE_1       :midi.C4,
            grand_staff.BASS_UPPER_LEDGER_SPACE_1      :midi.B3,
            grand_staff.BASS_LINE_5                    :midi.A3,
            grand_staff.BASS_SPACE_4                   :midi.G3,
            grand_staff.BASS_LINE_4                    :midi.F3,
            grand_staff.BASS_SPACE_3                   :midi.E3,
            grand_staff.BASS_LINE_3                    :midi.D3,
            grand_staff.BASS_SPACE_2                   :midi.C3,
            grand_staff.BASS_LINE_2                    :midi.B2,
            grand_staff.BASS_SPACE_1                   :midi.A2,
            grand_staff.BASS_LINE_1                    :midi.G2,
            grand_staff.BASS_UNDER_LEDGER_SPACE_1      :midi.F2,
            grand_staff.BASS_UNDER_LEDGER_LINE_1       :midi.E2,
            grand_staff.BASS_UNDER_LEDGER_SPACE_2      :midi.D2,
            grand_staff.BASS_UNDER_LEDGER_LINE_2       :midi.C2,
            grand_staff.BASS_UNDER_LEDGER_SPACE_3      :midi.B1,
            grand_staff.BASS_UNDER_LEDGER_LINE_3       :midi.A1,
            grand_staff.BASS_UNDER_LEDGER_SPACE_4      :midi.G1,
            grand_staff.BASS_UNDER_LEDGER_LINE_4       :midi.F1,
            grand_staff.BASS_UNDER_LEDGER_SPACE_5      :midi.E1,
            grand_staff.BASS_UNDER_LEDGER_LINE_5       :midi.D1,
            grand_staff.BASS_UNDER_LEDGER_SPACE_6      :midi.C1,
            grand_staff.BASS_UNDER_LEDGER_LINE_6       :midi.B0,
            grand_staff.BASS_UNDER_LEDGER_SPACE_7      :midi.A0
        };

        self.__midi_2_pos = {};
        for pos in self.__pos_2_midi:
            midi_note = self.__pos_2_midi[pos];
            if midi_note in self.__midi_2_pos:
                self.__midi_2_pos[midi_note] = self.__midi_2_pos[midi_note] + [pos]
            else:
                self.__midi_2_pos[midi_note] = [pos]

        self.__doremi_2_pos = {1:[],2:[],3:[],4:[],5:[],6:[],7:[]};

        for midi_note in self.__midi_2_pos:
            #middle c, c Major
            pos_C = grand_staff.TREBLE_UNDER_LEDGER_LINE_1;

            if midi_note%12 == self.__pos_2_midi[pos_C]%12:
                self.__doremi_2_pos[1] = self.__doremi_2_pos[1] + self.__midi_2_pos[midi_note];
            elif midi_note%12 == self.__pos_2_midi[pos_C - 1]%12:
                self.__doremi_2_pos[2] = self.__doremi_2_pos[2] + self.__midi_2_pos[midi_note];
            elif midi_note%12 == self.__pos_2_midi[pos_C - 2]%12:
                self.__doremi_2_pos[3] = self.__doremi_2_pos[3] + self.__midi_2_pos[midi_note];
            elif midi_note%12 == self.__pos_2_midi[pos_C - 3]%12:
                self.__doremi_2_pos[4] = self.__doremi_2_pos[4] + self.__midi_2_pos[midi_note];
            elif midi_note%12 == self.__pos_2_midi[pos_C - 4]%12:
                self.__doremi_2_pos[5] = self.__doremi_2_pos[5] + self.__midi_2_pos[midi_note];
            elif midi_note%12 == self.__pos_2_midi[pos_C - 5]%12:
                self.__doremi_2_pos[6] = self.__doremi_2_pos[6] + self.__midi_2_pos[midi_note];
            elif midi_note%12 == self.__pos_2_midi[pos_C - 6]%12:
                self.__doremi_2_pos[7] = self.__doremi_2_pos[7] + self.__midi_2_pos[midi_note];

if __name__ == '__main__':

    import painter

    import pygame.midi;
    pygame.midi.init();
    midi_device_id = 0;
    midi_out = pygame.midi.Output(midi_device_id);
    midi_out.set_instrument(1); #1 Acoustic Grand Piano

    x = painter.CPainter();

    xmap = CMidi_staff();

    from pygame.locals import *;
    import pygame

    pygame.fastevent.init();

    middle_c_pos = min(xmap.midi_2_pos(midi.C4))

    input_midi_devices = [];
    opened_midi_in = None;

    for i in range( pygame.midi.get_count() ):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r

            in_out = ""
            if input:
                in_out = "(input)"
                input_midi_devices.append(i)
            if output:
                in_out = "(output)"

            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))


    if len(input_midi_devices) > 0:
        opened_midi_in = pygame.midi.Input( input_midi_devices[0] );
    else:
        print "No MIDI input device";

    down_key = set();

    while True:
        if opened_midi_in and opened_midi_in.poll():
            midi_events = opened_midi_in.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, opened_midi_in.device_id)

            for m_e in midi_evs:
                pygame.fastevent.post( m_e )

        for event in pygame.fastevent.get():
            if event.type != MOUSEMOTION:
                print "fastevent:",event;

            if event.type == KEYDOWN:
                v = event.key - K_1 + 1
                if v in [1,2,3,4,5,6,7]:
                    down_key.add(v)
                    midi_out.note_on(xmap.pos_2_midi(middle_c_pos+1-v), 127)

            if event.type == KEYUP:
                v = event.key - K_1 + 1
                if v in down_key:
                    down_key.remove(v)
                    midi_out.note_off(xmap.pos_2_midi(middle_c_pos+1-v), 127)

            notes = [];
            for note in down_key:
                notes = notes + xmap.doremi_2_pos(note);
            x.update_asking_notes(notes);
            x.update_answering_notes(notes);

            if event.type == QUIT:
                pygame.midi.quit();
                pygame.quit();
                del midi_out;

                import sys;
                sys.exit()


