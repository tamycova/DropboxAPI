import unittest as u

loader = u.TestLoader().discover("./tests")
u.TextTestRunner().run(loader)
