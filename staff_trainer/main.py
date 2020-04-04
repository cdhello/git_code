import time;
from painter import CPainter;
import midi;
import grand_staff;
import pygame;
import pygame.midi;
from midi_staff_map import CMidi_staff;
import random;

from pygame.locals import *;

print K_KP0, K_KP1, K_KP2, K_KP9
print K_0, K_1,K_9

positions_to_train = [
    #grand_staff.TREBLE_UPPER_LEDGER_LINE_2      = 7
    #grand_staff.TREBLE_UPPER_LEDGER_SPACE_2     = 8
    #grand_staff.TREBLE_UPPER_LEDGER_LINE_1      = 9
    grand_staff.TREBLE_UPPER_LEDGER_SPACE_1 ,
    grand_staff.TREBLE_LINE_5               ,
    grand_staff.TREBLE_SPACE_4              ,
    grand_staff.TREBLE_LINE_4               ,
    grand_staff.TREBLE_SPACE_3              ,
    grand_staff.TREBLE_LINE_3               ,
    grand_staff.TREBLE_SPACE_2              ,
    grand_staff.TREBLE_LINE_2               ,
    grand_staff.TREBLE_SPACE_1              ,
    grand_staff.TREBLE_LINE_1               ,
    grand_staff.TREBLE_UNDER_LEDGER_SPACE_1 ,
    grand_staff.TREBLE_UNDER_LEDGER_LINE_1  ,
    grand_staff.BASS_UPPER_LEDGER_LINE_1    ,
    grand_staff.BASS_UPPER_LEDGER_SPACE_1   ,
    grand_staff.BASS_LINE_5                 ,
    grand_staff.BASS_SPACE_4                ,
    grand_staff.BASS_LINE_4                 ,
    grand_staff.BASS_SPACE_3                ,
    grand_staff.BASS_LINE_3                 ,
    grand_staff.BASS_SPACE_2

];

class CTrainer():

    def get_midi_input(self):
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

        return opened_midi_in;

    def get_asking_pos_note(self):
        index = random.randint(0, len(self.positions_to_train)-1);
        pos  = self.positions_to_train[index];
        note = self.midi_staff_map_o.pos_2_midi(pos);

        return (pos, note)

    def get_solfa_name_from_key(self, key):
        if key >= K_0 and key <= K_9:
            num = (key - K_0)%7;
        elif key >= K_KP0 and key <= K_KP9:
            num = (key - K_KP0)%7;
        else:
            num = -1

        if num == 0:
            return 7;
        else:
            return num

    def __init__(self, positions_to_train):
        self.positions_to_train = positions_to_train;
        self.asking_pos = None;
        self.asking_note = None
        self.answering_poss = [];
        self.midi_staff_map_o = CMidi_staff();
        self.gui = CPainter();

        pygame.mixer.init();
        print "pygame.mixer.get_init()",pygame.mixer.get_init()
        self.fail_music = pygame.mixer.Sound("./res/fail.wav")
        self.fail_music.set_volume(0.2)

        pygame.init();
        pygame.fastevent.init();
        pygame.midi.init();

        self.opened_midi_in = self.get_midi_input();
        midi_device_id = 0;
        self.midi_out = pygame.midi.Output(midi_device_id);

    def __del__(self):

        if self.opened_midi_in:
            del self.opened_midi_in;

        if self.midi_out:
            del self.midi_out;

        pygame.midi.quit()
        pygame.quit()

    def new_asking(self):
        if self.asking_note:
            self.midi_out.note_off(self.asking_note, 127);

        (self.asking_pos, self.asking_note) = self.get_asking_pos_note();
        self.midi_out.note_on(self.asking_note, 127);
        self.gui.update_asking_notes([self.asking_pos]);

    def run(self):

        self.new_asking();

        while True:
            result = False;
            if self.opened_midi_in and self.opened_midi_in.poll():
                midi_events = self.opened_midi_in.read(10)
                # convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, self.opened_midi_in.device_id)

                for m_e in midi_evs:
                    pygame.fastevent.post( m_e )

            #for event in pygame.event.get():
            for event in pygame.fastevent.get():

                if event.type == QUIT:
                    return;

                elif event.type == KEYDOWN:

                    v = self.get_solfa_name_from_key(event.key);
                    if v > 0:
                        p_list = self.midi_staff_map_o.doremi_2_pos(v);
                        for p in p_list:
                            if p in self.positions_to_train:
                                self.answering_poss.append(p);
                        if len(self.answering_poss) == 0:
                            self.gui.update_result(result);
                            if result:
                                self.new_asking();
                            else:
                                self.fail_music.play();
                    else: # replay the asking note if other key
                        self.midi_out.note_off(self.asking_note, 127);
                        self.midi_out.note_on(self.asking_note, 127);

                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        return;

                    v = self.get_solfa_name_from_key(event.key);
                    if v > 0:
                        p_list = self.midi_staff_map_o.doremi_2_pos(v);
                        for p in p_list:
                            if p in self.answering_poss:
                                self.answering_poss.remove(p)
                                if p == self.asking_pos:
                                    result = True;
                        if len(self.answering_poss) == 0:
                            self.gui.update_result(result);
                            if result:
                                self.new_asking();
                            else:
                                self.fail_music.play();
                elif event.type == pygame.midi.MIDIIN and event.status != 144:
                    continue; #There are many midi non-key up/down event, ignore them

                elif event.type == pygame.midi.MIDIIN and event.status == 144 and event.data2 > 0:
                #<Event(34-Unknown {'status': 144, 'vice_id': 1, 'timestamp': 281097, 'data1': 53, 'data3': 0, 'data2': 35})>
                    p_list = self.midi_staff_map_o.midi_2_pos(event.data1);
                    for p in p_list:
                        self.answering_poss.append(p);

                        if len(self.answering_poss) == 0:
                            self.gui.update_result(result);
                            if result:
                                self.new_asking();
                            else:
                                self.fail_music.play();

                elif event.type == pygame.midi.MIDIIN and event.status == 144 and event.data2 == 0:
                #<Event(34-Unknown {'status': 144, 'vice_id': 1, 'timestamp': 281351, 'data1': 53, 'data3': 0, 'data2': 0})>
                    p_list = self.midi_staff_map_o.midi_2_pos(event.data1);
                    for p in p_list:
                        if p in self.answering_poss:
                            self.answering_poss.remove(p)
                            if p == self.asking_pos:
                                result = True;

                            if len(self.answering_poss) == 0:
                                self.gui.update_result(result);
                                if result:
                                    self.new_asking();
                                else:
                                    self.fail_music.play();

                self.gui.update_answering_notes(self.answering_poss);

if __name__ == '__main__':
    Trainer = CTrainer(positions_to_train);
    Trainer.run();
    del Trainer

