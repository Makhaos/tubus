Tubus web application (Proof of concept)
========================================

Python version 3.7.4  
Using Flask   
Deployed in Heroku and Amazon Web Services  
Available at [tubus.herokuapp.com](https://tubus.herokuapp.com/)

Setup:
----------------------
_The following instructions are to be used with a Linux machine_

### venv
I recommend using a venv (virtual environment) to install all dependencies and work in the web application from there.
### pip
Install pip packages: `pip install -r requirements.txt`  
### Redis Server
`sudo apt-get install redis-server`
### AWS (Amazon Web Services)
Install command line interface: `sudo apt install awscli`		
In the [AWS console](https://console.aws.amazon.com/iam/home?region=eu-north-1#/users), create an access key under the ESSIQ user. Don't forget to save the secret access key for the next step!		
Configuration: 		
`aws configure`	
```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUbPxRfiCYEXAMPLEKEY
Default region name [None]: eu-north-1
Default output format [None]:
```
### Heroku
Install command line interface: `curl https://cli-assets.heroku.com/install-ubuntu.sh | sh`  
Add Heroku's remote repository to your local repository: `heroku git:remote -a tubus` and login.

Run and deployment:
----------------------
### To run locally	   
Run `worker.py` for the redis background worker.		
Run `app.py`		
Open browser at localhost:5000 to access the application.
### To deploy to Heroku
`git push heroku master`	
OR from a branch besides master:	
`git push heroku testbranch:master`

Project description:
----------------------
Tubus System provides solutions for the renovation of different types of pipes.	  
Their procedure is to visualize a pipe inserting a camera through it and then evaluate the same pipe by watching the recorded video.    
Afterwards they provide a full report of their renovation to the customer.	    
Therefore a solution that could automate the evaluation process is what this project tries to achieve.    
This process envolves evaluating if the video is well recorded, regarding blurriness, as well as detection of harmful elements in the pipes.    


Web application description:
-------------------------------
This web application is using the Flask framework:		
`app.py` contains the flask application and the routes.	    
`worker.py` uses RQ (Redis Queue) that defines a worker to run in a different thread for queueing background processes: https://python-rq.org/	    
`Procfile` and `Aptfile` are both configurations for the deployment of the application to Heroku.   	
`templates` and `static` folders contain the front-end of the application (Bootstrap). The front-end was based of a free theme SB Admin 2: https://startbootstrap.com/themes/sb-admin-2/	    
`common` folder is for utilities used across the project and for the manager of AWS.	    
`src` folder englobes the application functionality and algorithms.   

### Functionality and Algorithms
This section is related to the functionality of the videos evaluation.	    
`main.py` maintains all the functionality modules. The module to be called from the outside.	    
`video_to_frames.py` as the name indicates, it will fabricate pictures (frames) from a video.	    
`blur.py` is an algorithm based on the skimage library that calculates the Gaussian Blur of a frame to indicate a certain blurriness value. It also calls the AWS database to upload the results.	    
`color_detection.py` creates frames with a mask related to a certain color. A yellow detector function is used based on the yellow material Tubus uses to cover the renovated pipes.	    
`identify_pixels.py` outputs a CSV file that contains the variance of black pixels vs colored pixels from a masked frame that only has these 2 types of pixel.    
The ambition is to identify if the pipe was well renovated with enough yellow material around the pipe.		    
`identify_circles.py` purpose is to identify the hole of the pipe, by plotting a circle in its edge, in order to know if the video is being recorded in a centered view.    
