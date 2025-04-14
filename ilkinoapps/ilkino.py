import random
import os
from abc import abstractmethod
from datetime import datetime
import tkinter as tk


# SEATS --------------------------------------------------------------------------------------

# Objek standard seat
class Seat:
    def __init__(self, seat_number):
        # property: num, status
        self.seat_number = seat_number
        self.booked_status = False

    def book_seat(self):
        # Jika belum di-booked
        if self.booked_status == False:
            self.booked_status = True
        # Jika sudah di-booked
        else: 
            print("This seat is occupied!")

    # def __str__(self):
    #     # Format print
    #     return f"Seat Number: {self.seat_number}, Booked Status: {self.booked_status}, Gift Status: {self.gift_status}"


# Objek special seat
class SpecialSeat(Seat):
    def __init__(self, seat_number, __gift):
        super().__init__(seat_number)
        # Private. 
        rd = random.sample(range(0,len(__gift)), 1)
        self.gift = __gift[rd[0]]
        
    def get_gift(self):
        return self.gift
        

# PRINTER --------------------------------------------------------------------------------------

class Generator:
    @abstractmethod
    def generate():
        return[]


class MockGenerator(Generator):
    def generate():
        return[1, 3, 5, 7, 9, 2, 4, 6, 8, 10]


class RealGenerator(Generator):
    def generate():
        return random.sample(range(1,37,2),5) + random.sample(range(2,38,2),5)
    

class Printer:
    @abstractmethod
    def print_special_ticket(self):
        pass
    def print_ticket(self):
        pass

class MockPrinter(Printer):
    def print_special_ticket(self, name, seats):
        str_seat1 = '_'.join([str(_) for _ in seats])
        str_seat2 = ','.join([str(_) for _ in seats])
        
        print(f"Seat {str_seat2} is booked by {name.title()}.")
        print(f"Receipt {name.title()}_{str_seat1}.txt is printed. Don't loose your ticket.")
        return 'Printed Special Ticket'
    
    def print_ticket(self, name, seats):
        str_seat1 = '_'.join([str(_) for _ in seats])
        str_seat2 = ','.join([str(_) for _ in seats])
        
        print(f"Seat {str_seat2} is booked by {name.title()}.")
        print(f"Receipt {name.title()}_{str_seat1}.txt is printed. Don't loose your ticket.")
        return 'Printed Ticket'

class RealPrinter(Printer):
    def print_special_ticket(self, name, seats):
        str_seat1 = '_'.join([str(_) for _ in seats])
        str_seat2 = ','.join([str(_) for _ in seats])
        
        print(f"Seat {str_seat2} is booked by {name.title()}.")
        print(f"Receipt {name.title()}_{str_seat1}.txt is printed. Don't loose your ticket.")

        with open(f'{name.title()}_{str_seat1}', 'w') as f:
            f.write(
                f'--------------- IL Kino Receipt ---------------\n'
                f'Name: {name.title()}\n'
                f'Seats Number: {str_seat2}\n'
                f'Please check below your seat to get your gift.\n'
                f'Please arrive 15 minutes before.'
            )
    
    def print_ticket(self, name, seats):
        str_seat1 = '_'.join([str(_) for _ in seats])
        str_seat2 = ','.join([str(_) for _ in seats])

        print(f"Seat {str_seat2} is booked by {name.title()}.")
        print(f"Receipt {name.title()}_{str_seat1}.txt is printed. Don't loose your ticket.")

        with open(f'{name.title()}_{str_seat1}', 'w') as f:
            f.write(
                f'--------------- IL Kino Receipt ---------------\n'
                f'Name: {name.title()}\n'
                f'Seats Number: {str_seat2}\n'
                f'Please arrive 15 minutes before.'
            )

# CINEMA --------------------------------------------------------------------------------------

# Objek cinema
class Ilkino:
    def __init__(self, generated: list, printer):
        # Menampung object kursi
        self.seats = [] 
        # Buku bookingan. Berisi nama + seat number
        self.cinema_book = {}
        # Jumlah bookingan dalam jam tertentu
        self.time_report = {}
        # List random number
        self.ls_of_generated_random_number = generated
        # Untuk print tiket
        self.printer = printer

        self.app_run = True


    def booking(self, name, seats):
        # List confirmed booking
        success_booking = []
         
        for seat_number in seats:
            if seat_number <= 36:
                # Ter-reservasi
                if self.seats[seat_number - 1].booked_status == True:
                    print(f"Seat {seat_number} have been reserved. Your reservation is invalid. Please repeat the booking process.")
                    booked = False
                    return booked
                # Tdk ter-reservasi
                else:
                    success_booking.append(seat_number)
                    self.seats[seat_number - 1].booked_status = True
            # Invalid input
            else:
                print("Please insert valid input!")
                return 'Seat number is not valid!'

        # Nama = key di buku reservasi
        booked_names_ls = list(self.cinema_book.keys())
        if name in booked_names_ls:
            # Sudah ada 
            self.cinema_book[name] += success_booking
        # Case belum ada, tambah nama sebagai key di buku reservasi
        else:
            self.cinema_book[name] = success_booking

        now = datetime.now()
        # Hour saja. 
        current_time = now.strftime("%H:00")

        # Waktu = key di report
        booking_time_ls = list(self.time_report.keys())
        if current_time in booking_time_ls:
            # Case sudah ada. Tambah seat sesuai pesanan (makanya tidak bisa += 1).     >> Ketika jam sudah ada, tinggal append. 
            self.time_report[current_time] += len(success_booking)
        else:
            # Case belum ada. 
            self.time_report[current_time] = len(success_booking)
        
        # Jika ada yg dapet gift, print special. Else, standard
        if any(i in self.ls_of_generated_random_number for i in success_booking):
            self.printer.print_special_ticket(name, success_booking)
        else:
            self.printer.print_ticket(name, success_booking)
        
        booked = True
        return booked

    # find 
    def find_by_name(self, find):
        booked_names_ls = list(self.cinema_book.keys())
        if find in booked_names_ls:
            print(f"{find.title()} has booked seat(s) number {self.cinema_book[find]}.")
            return True
        else:
            print(f"{find.title()} has not booked any seats.")
            return False

    # Dictionary
    def get_booked_by_hour(self, hour):
        booking_time_ls = list(self.time_report.keys())
        if hour in booking_time_ls:
            print(f"At {hour}, {self.time_report[hour]} booking(s) was made.")
        else:
            print(f"No booking was made at {hour}.")

    # Untuk print list gift yg akan keluar
    def get_all_distributed_gift(self):
        self.gift_seats = []
        for seat in self.seats:
            if seat.seat_number in self.ls_of_generated_random_number:
                if seat.booked_status == True:
                    self.gift_seats.append([seat.seat_number, seat.get_gift()])
                    # gift_seats.(seat_number = seat.get_gift())
        # print(gift_seats)
        for seat, gift in self.gift_seats:
            gift_split = gift.replace("_", " ")
            print(f"{seat} - {gift_split.title()}")
        return 

    
    def get_report(self):
        print("\nHour\tNumber of Booking")
        for time, booking_number in self.time_report.items():
            print(f"{time}\t{booking_number}")
        print("\nAll distributed SeatNumber - Gift:")
        self.get_all_distributed_gift()
        return self.time_report

    
    def GUI(self): 
        def choice_one():
            def book(name,seat_num):
                name = name_entry.get().lower()
                seat_num = list(map(int, seat_number_entry.get().split(",")))
                
                b = self.booking(name,seat_num)
                if b is True:
                    str_seat1 = '_'.join([str(_) for _ in seat_num])
                    str_seat2 = ', '.join([str(_) for _ in seat_num])

                    frame = tk.Frame(seatBooking)
                    frame.grid(rowspan=2, row=3, column=0, sticky='w')
                    output = tk.Label(frame, text=f"Seat {str_seat2} is booked by {name.title()}.", font='50')
                    output.grid(row=0,pady=3)
                    output1 = tk.Label(frame, text=f"Receipt {name.title()}_{str_seat1}.txt is printed. Don't loose your ticket.", font='50')
                    output1.grid(row=1, pady=3)

                elif b is False:
                    str_seat2 = ', '.join([str(_) for _ in seat_num])

                    frame = tk.Frame(seatBooking)
                    frame.grid(rowspan=2, row=3, column=0, sticky='w')
                    output = tk.Label(frame, text=f"Seat {str_seat2} have been reserved.", font='50')
                    output.grid(row=0, pady=3)
                    output1 = tk.Label(frame, text=f"Your reservation is invalid. Please repeat the booking process.", font='50')
                    output1.grid(row=1, pady=3)
            
            def close_btn():
                seatBooking.destroy()
                seatBooking.update()
                ilkinoApp.destroy()
                ilkinoApp.update()
 
            seatBooking = tk.Toplevel()
            seatBooking.title("Seat Booking")
            seatBooking.geometry("500x200")

            title1 = tk.Label(seatBooking, text='Seat Booking', font='72')
            title1.grid(row=0, pady=5, sticky='ew')

            frame = tk.Frame(seatBooking)
            frame.grid(row=1, column=0, sticky='w')

            seat_number_input = tk.Label(frame, text='Seat Number', font='50')
            seat_number_input.grid(row=0, column=0,sticky='w')

            title_1 = tk.Label(frame, text=':', font='50')
            title_1.grid(row=0, column=2)

            seat_number_entry = tk.Entry(frame, width=30)
            seat_number_entry.grid(row=0, column=3, padx=20)

            name_input = tk.Label(frame, text='Name', font='50')
            name_input.grid(row=1, column=0, sticky='w')

            title_2 = tk.Label(frame, text=':', font='50')
            title_2.grid(row=1, column=2)

            name_entry = tk.Entry(frame, width=30)
            name_entry.grid(row=1, column=3, padx=20)

            pembatas1 = tk.Label(seatBooking, text='', font='50')
            pembatas1.grid(row=3, padx=6)

            pembatas2 = tk.Label(seatBooking, text='', font='50')
            pembatas2.grid(row=4)
            
            frame1 = tk.Frame(seatBooking)
            frame1.grid(row=5, column=0, sticky='w')

            input_bttn = tk.Button(frame1, text='Input', width=7,command=lambda:book(name_entry, seat_number_entry), font="Verdana 14 underline", bg="light blue", relief="groove")
            input_bttn.grid(row=0, column=0,sticky='e')

            exit_bttn = tk.Button(frame1, text='Exit', width=7, font="Verdana 14 underline", bg="light blue", relief="groove", command=close_btn)
            exit_bttn.grid(row=0, column=1,sticky='w')        

        def choice_two():
            def close_btn():
                findByName.destroy()
                findByName.update()
                ilkinoApp.destroy()
                ilkinoApp.update()

            def find(name):
                name = name.get()
                name = name.lower()

                f = self.find_by_name(name)
                
                if f is True:
                    str_seat = ', '.join([str(_) for _ in self.cinema_book[name]])
                    batas = ' '*1000
                    pembatas1 = tk.Label(findByName, text=batas, font='50')
                    pembatas1.grid(row=3, pady=30)
                    output = tk.Label(findByName, text=f"{name.title()} has booked seat(s) number {str_seat}.", font='50')
                    output.grid(row=3, sticky='w', pady=30)
                else:
                    batas = ' '*1000
                    pembatas1 = tk.Label(findByName, text=batas, font='50')
                    pembatas1.grid(row=3, pady=30)
                    output = tk.Label(findByName, text=f"{name.title()} has not booked any seats.", font='50')
                    output.grid(row=3, sticky='w', pady=30)


            findByName = tk.Toplevel()
            findByName.title("Search")
            findByName.geometry("400x200")

            title1 = tk.Label(findByName, text='Find', font='72')
            title1.grid(row=0, pady=5, sticky='ew')

            frame0 = tk.Frame(findByName)
            frame0.grid(row=1, column=0, sticky='w')

            name_input = tk.Label(frame0, text='Name to Find', font='50')
            name_input.grid(row=0, column=0,sticky='w')

            title_1 = tk.Label(frame0, text=':', font='50')
            title_1.grid(row=0, column=2)
            
            name_entry = tk.Entry(frame0, width=30)
            name_entry.grid(row=0, column=3, padx=20)

            pembatas1 = tk.Label(findByName, text='', font='50')
            pembatas1.grid(row=3, pady=30)

            frame1 = tk.Frame(findByName)
            frame1.grid(row=4, column=0, sticky='w')

            input_bttn = tk.Button(frame1, text='Input', width=7,command=lambda:find(name_entry), font="Verdana 14 underline", bg="light blue", relief="groove")
            input_bttn.grid(row=0, column=0,sticky='ew')

            exit_bttn = tk.Button(frame1, text='Exit', width=7, font="Verdana 14 underline", bg="light blue", relief="groove", command=close_btn)
            exit_bttn.grid(row=0, column=1,sticky='ew')   

        def choice_three():
            def close_btn():
                report.destroy()
                report.update()
                ilkinoApp.destroy()
                ilkinoApp.update()

            self.get_report()

            times = []
            total_booking = []
            for time, booking_number in self.time_report.items():
                times.append(time)
                total_booking.append(booking_number)

            seat_with_gift = []
            gifts =[]
            for seat, gift in self.gift_seats:
                seat_with_gift.append(seat)
                gifts.append(gift)

            report = tk.Toplevel()
            report.title("Search")
            report.geometry("360x550")

            title1 = tk.Label(report, text='Report', font='72')
            title1.grid(row=0, pady=5, columnspan=2, sticky='ew')

            frame1 = tk.Frame(report)
            frame1.grid(row=1, columnspan=2, sticky='w')

            hour = tk.Label(frame1, text='Hour', font='50')
            hour.grid(row=0, column=0,sticky='w')

            number_of_booking = tk.Label(frame1, text='Number of Booking(s)', font='50')
            number_of_booking.grid(row=0, column=1,sticky='w')

            for i in range(len(times)):
                label = tk.Label(frame1, text=times[i], font='50')
                label.grid(row=i+1, column=0,sticky='w')

                label1 = tk.Label(frame1, text=total_booking[i], font='50')
                label1.grid(row=i+1, column=1,sticky='w')

            pembatas1 = tk.Label(report, text='', font='50')
            pembatas1.grid(row=2)

            pembatas1 = tk.Label(report, text='All distributed SeatNumber - Gift: ', font='50')
            pembatas1.grid(row=3)

            frame2 = tk.Frame(report)
            frame2.grid(row=4, column=0, sticky='w')

            for i in range(len(seat_with_gift)):
                label = tk.Label(frame2, text=seat_with_gift[i], font='50')
                label.grid(row=i+1, column=0,sticky='w')

                dash = tk.Label(frame2, text=' - ', font='50')
                dash.grid(row=i+1, column=1,sticky='w')

                label1 = tk.Label(frame2, text=gifts[i], font='50')
                label1.grid(row=i+1, column=2,sticky='w')



            exit_bttn = tk.Button(report, text='Exit', width=7, font="Verdana 14 underline", bg="light blue", relief="groove", command=close_btn)
            exit_bttn.grid(row=50, column=1,sticky='ew')     


        def exit():
            ilkinoApp.destroy()
            ilkinoApp.update()
            self.app_run = False
        
        gui = []
        for i in range(0, 36):
            if self.seats[i].__class__.__name__ == 'SpecialSeat' and self.seats[i].booked_status == True:
                gui.append('G')
            elif self.seats[i].__class__.__name__ == 'Seat' and self.seats[i].booked_status == True:
                gui.append('X')
            else:
                gui.append(f'{i + 1}')

        ilkinoApp = tk.Tk()
        ilkinoApp.title('Ilkino Cinema App')
        ilkinoApp.geometry("360x550")


        title1 = tk.Label(ilkinoApp, text='IlKino', font='50')
        title1.grid(row=0, columnspan=350)
        title2 = tk.Label(ilkinoApp, text='Nansenstrasse 22,', font='50')
        title2.grid(row=1, columnspan=350, sticky='ew')
        title3 = tk.Label(ilkinoApp, text='12047 Berlin', font='50')
        title3.grid(row=2, columnspan=350, sticky='ew')
        screen_label = tk.Label(ilkinoApp, text='SCREEN', font='50', background='gray')
        screen_label.grid(row=6, columnspan=350, pady=10, sticky='ew')

        # frame_kiri = 
        satu = tk.Label(ilkinoApp, text=f"{gui[0]}", font='50')
        satu.grid(row=7, column=0, pady=5, padx= 15, sticky='ew')

        tiga = tk.Label(ilkinoApp, text=gui[2], font='50')
        tiga.grid(row=7, column=1, pady=5, padx= 15, sticky='ew')

        lima = tk.Label(ilkinoApp, text=gui[4], font='50')
        lima.grid(row=7, column=2, pady=5, padx= 15, sticky='ew')

        pembatas = tk.Label(ilkinoApp, text='', font='50')
        pembatas.grid(row=7, column=3, pady=5, padx= 15, sticky='ew')

        dua = tk.Label(ilkinoApp, text=gui[1], font='50')
        dua.grid(row=7, column=4, pady=5, padx= 15, sticky='e')

        empat = tk.Label(ilkinoApp, text=gui[3], font='50')
        empat.grid(row=7, column=5, pady=5, padx= 15, sticky='ew')

        enam = tk.Label(ilkinoApp, text=gui[5], font='50')
        enam.grid(row=7, column=6, pady=5, padx= 15, sticky='ew')


        tujuh = tk.Label(ilkinoApp, text=gui[6], font='50')
        tujuh.grid(row=8, column=0, pady=5, padx= 15, sticky='ew')

        sembilan = tk.Label(ilkinoApp, text=gui[8], font='50')
        sembilan.grid(row=8, column=1, pady=5, padx= 15, sticky='ew')

        sebelas = tk.Label(ilkinoApp, text=gui[10], font='50')
        sebelas.grid(row=8, column=2, pady=5, padx= 15, sticky='ew')

        delapan = tk.Label(ilkinoApp, text=gui[7], font='50')
        delapan.grid(row=8, column=4, pady=5, padx= 15, sticky='e')

        sepuluh = tk.Label(ilkinoApp, text=gui[9], font='50')
        sepuluh.grid(row=8, column=5, pady=5, padx= 15, sticky='ew')

        duabelas = tk.Label(ilkinoApp, text=gui[11], font='50')
        duabelas.grid(row=8, column=6, pady=5, padx= 15, sticky='ew')


        tigabls = tk.Label(ilkinoApp, text=gui[12], font='50')
        tigabls.grid(row=9, column=0, pady=5, padx= 15, sticky='ew')

        limabls = tk.Label(ilkinoApp, text=gui[14], font='50')
        limabls.grid(row=9, column=1, pady=5, padx= 15, sticky='ew')

        tujuhbelas = tk.Label(ilkinoApp, text=gui[16], font='50')
        tujuhbelas.grid(row=9, column=2, pady=5, padx= 15, sticky='ew')

        empatbls = tk.Label(ilkinoApp, text=gui[13], font='50')
        empatbls.grid(row=9, column=4, pady=5, padx= 15, sticky='e')

        enambls = tk.Label(ilkinoApp, text=gui[15], font='50')
        enambls.grid(row=9, column=5, pady=5, padx= 15, sticky='ew')

        delapanbelas = tk.Label(ilkinoApp, text=gui[17], font='50')
        delapanbelas.grid(row=9, column=6, pady=5, padx= 15, sticky='ew')


        sembilanbls = tk.Label(ilkinoApp, text=gui[18], font='50')
        sembilanbls.grid(row=10, column=0, pady=5, padx= 15, sticky='ew')

        duasatu = tk.Label(ilkinoApp, text=gui[20], font='50')
        duasatu.grid(row=10, column=1, pady=5, padx= 15, sticky='ew')

        duatiga = tk.Label(ilkinoApp, text=gui[22], font='50')
        duatiga.grid(row=10, column=2, pady=5, padx= 15, sticky='ew')

        duaplh = tk.Label(ilkinoApp, text=gui[19], font='50')
        duaplh.grid(row=10, column=4, pady=5, padx= 15, sticky='e')

        duadua = tk.Label(ilkinoApp, text=gui[21], font='50')
        duadua.grid(row=10, column=5, pady=5, padx= 15, sticky='ew')

        duaempat = tk.Label(ilkinoApp, text=gui[23], font='50')
        duaempat.grid(row=10, column=6, pady=5, padx= 15, sticky='ew')


        dualima = tk.Label(ilkinoApp, text=gui[24], font='50')
        dualima.grid(row=11, column=0, pady=5, padx= 15, sticky='ew')

        duatujuh = tk.Label(ilkinoApp, text=gui[26], font='50')
        duatujuh.grid(row=11, column=1, pady=5, padx= 15, sticky='ew')

        duasembilan = tk.Label(ilkinoApp, text=gui[28], font='50')
        duasembilan.grid(row=11, column=2, pady=5, padx= 15, sticky='ew')

        duaenam = tk.Label(ilkinoApp, text=gui[25], font='50')
        duaenam.grid(row=11, column=4, pady=5, padx= 15, sticky='e')

        duaselapan = tk.Label(ilkinoApp, text=gui[27], font='50')
        duaselapan.grid(row=11, column=5, pady=5, padx= 15, sticky='ew')

        tigapuluh = tk.Label(ilkinoApp, text=gui[29], font='50')
        tigapuluh.grid(row=11, column=6, pady=5, padx= 15, sticky='ew')


        tiga1 = tk.Label(ilkinoApp, text=gui[30], font='50')
        tiga1.grid(row=12, column=0, pady=5, padx= 15, sticky='ew')

        tiga3 = tk.Label(ilkinoApp, text=gui[32], font='50')
        tiga3.grid(row=12, column=1, pady=5, padx= 15, sticky='ew')

        tiga5 = tk.Label(ilkinoApp, text=gui[34], font='50')
        tiga5.grid(row=12, column=2, pady=5, padx= 15, sticky='ew')

        tiga2 = tk.Label(ilkinoApp, text=gui[31], font='50')
        tiga2.grid(row=12, column=4, pady=5, padx= 15, sticky='e')

        tiga4 = tk.Label(ilkinoApp, text=gui[33], font='50')
        tiga4.grid(row=12, column=5, pady=5, padx= 15, sticky='ew')

        tiga6 = tk.Label(ilkinoApp, text=gui[35], font='50')
        tiga6.grid(row=12, column=6, pady=5, padx= 15, sticky='ew')

        pembatas1 = tk.Label(ilkinoApp, text='', font='50')
        pembatas1.grid(row=13)
        
        # Create buttons for the menu options
        booking_button = tk.Button(ilkinoApp, text="1. Seat Booking", font="Verdana 11", bg="gray", relief="groove", command=lambda: choice_one())
        find_by_name_button = tk.Button(ilkinoApp, text="2. Find By Name", font="Verdana 11", bg="gray", relief="groove", command=lambda: choice_two())
        report_button = tk.Button(ilkinoApp, text="3. Report", font="Verdana 11", bg="gray", relief="groove", command=lambda:choice_three())
        exit_button = tk.Button(ilkinoApp, text="4. Exit", font="Verdana 11", bg="gray", relief="groove", command=exit)
        
        # # Place the buttons on the grid
        booking_button.grid(row=14, column=0, columnspan=6, sticky='w', pady=5)
        find_by_name_button.grid(row=15, column=0, columnspan=6, sticky='w', pady=5)
        report_button.grid(row=16, column=0, columnspan=6, sticky='w', pady=5)
        exit_button.grid(row=17, column=0, columnspan=6, sticky='w', pady=5)
        
        ilkinoApp.mainloop()

    def setup(self, __gift: list):
        # Siapkan special seats and standard seats
        for number in range(1, 37):
            if number in self.ls_of_generated_random_number:
                self.seats.append(SpecialSeat(number, __gift))
            else:
                self.seats.append(Seat(number))

    def run(self):
        while self.app_run:
            self.GUI()
