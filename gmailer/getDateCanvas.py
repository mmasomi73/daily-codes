from datetime import datetime, timezone
from canvas_lms_api import Canvas
import pandas as pd
import jdatetime
import datetime
import json
import pytz


class CanvasHandler:
    _TOKEN = "xxxxxxxx"
    course_id = 'xxxx'
    assignment_id = 'xxxx'

    def getUsersList(self, filename):
        grader = Canvas(base="https://cw1.basu.ac.ir/", token=self._TOKEN)
        grader.course_id = self.course_id

        users = grader.GetCourseUsers()
        users = pd.DataFrame(users)
        users.to_csv(filename)

    def getSubmissionsFromAPI(self):
        grader = Canvas(base="https://cw1.basu.ac.ir/", token=self._TOKEN)
        grader.course_id = self.course_id

        subs_obj = grader.GetCourseAssignmentSubmissions(self.assignment_id)

        submissions_list = [['STD_ID', 'Submit', 'Late']]
        for sub_obj in subs_obj:

            user_number = self.findUserByID(int(sub_obj['user_id']))
            submitted_at = self.j_dater(sub_obj['submitted_at'])
            has_late = sub_obj['late']
            submissions_list.append([user_number, submitted_at, has_late])
        return submissions_list

    def getSubmissionsFromFile(self, path):
        subs_plain = open(path, "r")
        subs_obj = json.loads(subs_plain.read())

        submissions_list = [['STD_ID', 'Submit', 'Late']]
        for sub_obj in subs_obj:
            user_number = self.findUserByID(int(sub_obj['user_id']))
            submitted_at = self.j_dater(sub_obj['submitted_at'])
            has_late = sub_obj['late']
            submissions_list.append([user_number, submitted_at, has_late])
        return submissions_list

    def putSubmissionsList(self, path, filename):
        submissions_list = self.getSubmissionsFromFile(path)
        # submissions_list = self.getSubmissionsFromAPI()
        submissions_df = pd.DataFrame(submissions_list)
        submissions_df.to_csv(filename, encoding='utf-8')

    def findUserByID(self, id):
        users = pd.read_csv('user_lists.csv', encoding='utf-8')
        user = users[users['id'] == id]

        mma = user['login_id'].astype(str)
        if mma.values.shape[0] <= 0:
            return str(id)

        return str(mma.values[0]).replace('.0', '')

    def j_dater(self, submitted_at):
        if len(str(submitted_at)) <= 5:
            return '-'

        date = datetime.datetime.strptime(submitted_at, '%Y-%m-%dT%H:%M:%S%z')
        new_timezone = pytz.timezone("Asia/Tehran")
        date = date.astimezone(new_timezone)
        date = jdatetime.datetime.fromgregorian(datetime=date)
        return date.strftime('%Y/%m/%d %H:%M')


cnv = CanvasHandler()
cnv.putSubmissionsList('Ex-02.json', 'Ex-02-List.csv')
