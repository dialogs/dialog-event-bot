class User:
    def __init__(self, id_, name=None, surname=None, org=None, post=None, e_mail=None, phone=None):
        self.id_ = id_
        self.name = name
        self.surname = surname
        self.org = org
        self.post = post
        self.phone = phone
        self.e_mail = e_mail
        self.last_key = ""
        self.lock_msg = False

    def is_full_profile(self):
        if self.id_ and self.name and self.surname and self.org and self.post and self.phone and self.e_mail:
            return True
        return False

    def form(self):
        return "{0} {1}\n" \
               "{2}\n" \
               "{3}\n" \
               "{4}\n"\
               "{5}".format(self.name, self.surname, self.org, self.post, self.e_mail, self.phone)

    def filling_data(self, last_key, data):
        if last_key == "hello" or last_key == "second_name":
            self.name = data
        elif last_key == "surname" or last_key == "second_surname":
            self.surname = data
        elif last_key == "org":
            self.org = data
        elif last_key == "post":
            self.post = data
        elif last_key == "e-mail":
            self.e_mail = data
        elif last_key == "phone":
            self.phone = data
