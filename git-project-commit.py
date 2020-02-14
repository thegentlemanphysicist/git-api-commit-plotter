import requests
import matplotlib.pyplot as plt
import sys
import time
import datetime

# The first arg 
resp = requests.get("http://api.github.com/repos/bcgov/%s/stats/contributors" %(str(sys.argv[1])))

# Project graduation date
# Test date october 1st 2019
if len(sys.argv)>2:
    timeStampGraduation = time.mktime(datetime.datetime.strptime((str(sys.argv[2])), "%d/%m/%Y").timetuple()) 
else:
    timeStampGraduation = None

# Parse out the git commits and plot them
totalCommits = None


for contributor in resp.json():
    # The contributors login name is
    author=contributor['author']['login']
    print(author)
    # The contributions per week is
    contributions=contributor['weeks']

    commitsPerWeek=[(contribution['w'],contribution['c']) for contribution in contributions]
    
    # Plots zeroed at the graduation date of the project
    if timeStampGraduation:
        weeks = [(contribution['w']-timeStampGraduation)/604800 for contribution in contributions]
    else:
        # Weeks is measured since the start of the project.
        # Plots start at the start of the project
        weeks = [(contribution['w']-contributions[0]['w'])/604800 for contribution in contributions]
    
    commits = [contribution['c'] for contribution in contributions]
    plt.plot(weeks,commits)

    if totalCommits:
        totalCommits = [sum(x) for x in zip(totalCommits,commits)]
    else:
        totalCommits = [x for x in commits]


# Print the total number of commits in a different style
plt.plot(weeks,totalCommits,linestyle='--', color='black')

# naming the x axis 
plt.xlabel('Weeks Since Graduation') 
# naming the y axis 
plt.ylabel('Commit Number') 
# giving a title to my graph 
plt.title('Commits per week') 

# show a legend on the plot 
plt.legend() 

# function to show the plot 
plt.show()