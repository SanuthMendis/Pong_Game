from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

#Creating class PongPaddor()
class PongPaddle(Widget):
    score = NumericProperty(0)
    #Defining bounce_ball method to calculate how ball should bounce
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

#Creating class PongBall()
class PongBall(Widget):
    #giving velocity of bith x and y diections
    #Using ReferenceListProperty(velocity_x, velocity_y) to refer both x and y velocities at the same time
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    #defining move method to calculate the latest position of the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

#Creating class PongGame()
class PongGame(Widget):
    #using ObjectProperty() to tell to refer to the pong.kv file
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    #creating the serve_ball method and moving the ball from center according to the given velocity
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

   #moving the ball by calling the move(), bounce_ball() methods and updating th score
    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # calculating the score of each p[layers when ball went off the players pads
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
#Defining on_touch_move() method to defing how the players touch the ball
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

#Creating the PongApp(App) class and created an instance of the PongGame() and call serve_ball() method
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        #using clock function to define the number of frames that has to be shown in 1 second
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()