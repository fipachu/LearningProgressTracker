"""Learning Progress Tracker


Example student_data dict with one student inside:
{
    752001:
        {
            'email': 'c@d.e',
            'first name': 'Aa',
            'last name': 'Bb',
            'points': [0, 1, 2, 3],
            'submissions': [0, 1, 1, 1]
        },
}
"""
from tracker import Tracker

if __name__ == "__main__":
    Tracker().cmdloop()
