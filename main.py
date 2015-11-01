import cgi
import os
import webapp2
import jinja2

from random import randint

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        newrand = randint(1,10)
        template_values = {
            'playermessage': 'Guess a random number between 1 and 10 (inclusive)',
            'currrand': newrand,
            'stillguessing': True,
            'guesscount': 0,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        stillguessing = True
        guesscount = int(self.request.get('guesscount')) + 1
        currrand = int(self.request.get('currrand'))
        try:
            currguess = int(self.request.get('guess'))
            if currguess == currrand:
                mesg = 'You guessed right on, ' + str(currrand) + ' was the number. Number of guesses: ' + str(guesscount)
                stillguessing = False
            if currguess < currrand:
                mesg = str(currguess) + ' is too low! Try again'
            if currguess > currrand:
                mesg = str(currguess) + ' is too high! Try again'
        except ValueError: 
            mesg = 'Please enter a number'

        template_values = {
            'playermessage': mesg,
            'currrand': currrand,
            'stillguessing': stillguessing,
            'guesscount': guesscount,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

