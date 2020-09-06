import threading
import logging
import pygame

from maplepy.config import Config
from maplepy.xml.displayxml import DisplayXml
from maplepy.nx.displaynx import DisplayNx
from maplepy.display.console import Console
from maplepy.display.loading import Loading

FLAGS = pygame.HWSURFACE | pygame.HWACCEL | pygame.SRCALPHA | pygame.RESIZABLE
CAMERA_SPEED = 4
STATE_LOADING = 0
STATE_DISPLAY = 1


class Game():

    def __init__(self, config_file):

        # Config
        self.config = Config.instance()
        self.config.init(config_file)
        self.width = self.config['width']
        self.height = self.config['height']
        self.loading_path = self.config['loading_path']
        self.asset_path = self.config['asset_path']
        self.asset_type = self.config['asset_type']
        self.map = self.config['map']

        # Start pygame
        pygame.init()
        pygame.mixer.init(frequency=44100,
                          size=-16,
                          channels=2,
                          allowedchanges=0)
        pygame.display.set_caption(self.config['caption'])
        icon = pygame.image.load(self.config['icon'])
        pygame.display.set_icon(icon)

        # Create pygame objects
        self.screen = pygame.display.set_mode((self.width, self.height), FLAGS)
        self.clock = pygame.time.Clock()

        # Handle different displays
        available_displays = {
            'nx': DisplayNx,
            'xml': DisplayXml
        }
        Display = available_displays[self.asset_type]

        # Create displays
        self.displays = {
            STATE_LOADING: Loading(self.width, self.height),
            STATE_DISPLAY: Display(self.width, self.height, self.asset_path)
        }

        # Game state
        self.threads = []
        self.state = STATE_DISPLAY
        self.running = False
        self.fps = 60
        self.pressed = {}

        # Console
        self.typing = False
        self.text = ''
        self.console = Console(200, 100)

    def get_state(self):

        if self.threads:
            return STATE_LOADING
        else:
            return self.state

    def handle_command(self, text):

        # Parse text
        command = text.split()
        if len(command) < 1:
            return

        # Process command
        try:
            cmd = command[0].lower()
            if cmd == 'loading':
                fn = self.displays[STATE_LOADING].load_images
                args = tuple(command[1:3])
                thread = threading.Thread(target=fn, args=args)
                thread.start()
                self.threads.append(thread)
            if cmd == 'map':
                fn = self.displays[STATE_DISPLAY].load_map
                args = tuple(command[1:2])
                thread = threading.Thread(target=fn, args=args)
                thread.start()
                self.threads.append(thread)
            if cmd == 'rand':
                fn = self.displays[STATE_DISPLAY].load_random_map
                thread = threading.Thread(target=fn)
                thread.start()
                self.threads.append(thread)
        except:
            logging.exception('Command failed')
            pass

    def handle_threads(self):

        # Get the result of the thread
        for thread in self.threads:
            if not thread.is_alive():
                thread.join()

        # Remove thread from list if not alive
        self.threads = [thread for thread in self.threads if thread.is_alive()]

    def handle_events(self):

        # Get current state
        state = self.get_state()

        # Handle pygame events
        for event in pygame.event.get():

            # Quit application
            if event.type == pygame.QUIT:
                pygame.event.clear()
                self.running = False

            # Resized
            if event.type == pygame.VIDEORESIZE:
                self.width = event.w
                self.height = event.h
                for _, display in self.displays.items():
                    display.resize(event.w, event.h)

            # Console input
            if state != STATE_LOADING and event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_ESCAPE:
                        self.typing = False
                        self.text = ''
                        pygame.key.set_repeat()
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.handle_command(self.text)
                        self.typing = False
                        self.text = ''
                    else:
                        self.text += event.unicode
                elif event.key == pygame.K_BACKQUOTE:
                    self.typing = True
                    self.text = ''
                    pygame.key.set_repeat(200)

        # Empty
        pygame.event.pump()

    def handle_inputs(self):

        # Prevent quickly pressed keys, remove if done
        self.pressed = {k: v-1 for k, v in self.pressed.items() if v > 1}

        # Get current state
        state = self.get_state()

        # Get inputs
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        mouse_input = pygame.mouse.get_pressed()
        key_input = pygame.key.get_pressed()

        # Camera movement
        if state == STATE_DISPLAY and mouse_input[2]:
            self.displays[state].move_view(-mouse_dx, -mouse_dy)
        if state == STATE_DISPLAY and key_input[pygame.K_UP]:
            self.displays[state].move_view(0, -CAMERA_SPEED)
        if state == STATE_DISPLAY and key_input[pygame.K_DOWN]:
            self.displays[state].move_view(0, CAMERA_SPEED)
        if state == STATE_DISPLAY and key_input[pygame.K_LEFT]:
            self.displays[state].move_view(-CAMERA_SPEED, 0)
        if state == STATE_DISPLAY and key_input[pygame.K_RIGHT]:
            self.displays[state].move_view(CAMERA_SPEED, 0)

    def run(self):

        # Setup loading display
        self.handle_command(
            f'loading {self.loading_path} loading.repeat.1 asdf adsf')

        # Setup initial map
        self.handle_command(f'map {self.map}')

        # Main loop
        self.running = True
        while self.running:

            # Get current state
            state = self.get_state()

            # Handle threads
            self.handle_threads()

            # Handle pygame events
            self.handle_events()

            # Handle inputs
            self.handle_inputs()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Render environment
            self.displays[state].update()
            self.displays[state].blit(self.screen)

            # Console
            if self.typing:
                self.console.blit(self.screen, self.text)

            # Update
            pygame.display.update()
            self.clock.tick(self.fps)
