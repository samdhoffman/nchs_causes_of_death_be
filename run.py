# Disclaimer: 
# I don't always feel it is necessary to use comments as they can be misleading as code changes over time
# For purposes of documenting the code structure and thought process I have included comments below

# This file will be responsible for running our application

from nchs_causes_of_death import app

# Run server
if __name__ == '__main__':
  app.run(debug=True)