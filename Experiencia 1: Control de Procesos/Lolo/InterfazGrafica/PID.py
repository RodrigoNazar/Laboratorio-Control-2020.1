import time


class PID:
    def __init__(self, Kp=0.01, Ki=0.08, Kd=0.05, Kw=0, voltmax=1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Kw = Kw
        self.umax = voltmax
        self.sample_time = 0
        self.current_time = time.time()
        self.last_time = self.current_time
        self.ref = 0
        self.P = 0
        self.I = 0
        self.D = 0
        self.last_error = 0
        self.u = 0
        self.v = 0

    def reset(self):
        self.P = 0
        self.I = 0
        self.D = 0
        self.last_error = 0
        self.u = 0
        self.v = 0
        self.current_time = time.time()
        self.last_time = self.current_time

    def update(self, value):
        error = self.ref - value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if delta_time < self.sample_time:
            time.sleep(self.sample_time - delta_time)

        self.P = self.Kp * error
        self.I += (self.Ki * error + self.Kw * (self.u - self.v)) * delta_time

        if delta_time > 0:
            self.D = self.Kd * delta_error / delta_time

        self.v = self.P + self.I + self.D

        if self.v > self.umax:
            self.u = self.umax
        elif self.v < -self.umax:
            self.u = -self.umax
        else:
            self.u = self.v

        self.last_time = self.current_time
        self.last_error = error
        return self.u

    def ctes(self):
        return [self.Kp, self.Ki, self.Kd, self.Kw]
