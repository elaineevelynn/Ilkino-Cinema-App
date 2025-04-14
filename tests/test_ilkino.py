from ilkinoapps.ilkino import *

def test_book_unbooked_seat():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['iPhone'])
    expected_to_be_False = ilkino.seats[12].booked_status
    ilkino.booking('Ros', [13])
    expected_to_be_True = ilkino.seats[12].booked_status
    assert expected_to_be_False == False and expected_to_be_True == True


def test_book_unknown_seat():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Oreo'])
    current = ilkino.booking('Jarjit', [1000])
    expected = 'Seat number is not valid!'
    assert current == expected

def test_book_booked_seat():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Teddy Bear'])

    excepted_1 = ilkino.booking("Tok Dalang", [5])
    excepted_2 = ilkino.booking("Uncle Mutu", [5])

    assert excepted_1 == True and excepted_2 == False

def test_book_seat_with_gift():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Cola'])
    ilkino.booking("Ying", [2])

    current = ilkino.seats[1].__class__.__name__
    expected = 'SpecialSeat'

    assert current == expected

def test_get_book_by_hour():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Mcflurry'])
    ilkino.booking('Fizi', [2])
    ilkino.booking('Opah', [6])
    now = datetime.now()
    current_time = now.strftime("%H:00")
    a = ilkino.get_report()
    assert a[current_time] == 2

def test_get_all_distributed_gifts():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Nipis Madu'])
    ilkino.booking('Gopal', [2,3,4])
    ilkino.get_all_distributed_gift()

def test_search_booked_name():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Emas 5kg'])
    ilkino.booking('Meimei',[23])

    current = ilkino.find_by_name('Meimei')
    expected = True

    assert current == expected

def test_search_unbooked_name():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter())
    ilkino.setup(['Tisu'])
    ilkino.booking('Meimei',[23])
    ilkino.booking('Ehsan',[23])
    
    current = ilkino.find_by_name('Ehsan')
    expected = False
    
    assert current == expected

def test_gift_randomly_assigned_left():
    ilkino = Ilkino(MockGenerator.generate(), MockGenerator())
    ilkino.setup(['Surat Tanah'])

    current = False
    for i in range(1, 37, 2):
        if i in ilkino.ls_of_generated_random_number:
            current = True
            break
    
    expected = True

    assert current == expected

def test_gift_randomly_assigned_right():
    ilkino = Ilkino(MockGenerator.generate(), MockPrinter)
    ilkino.setup('Surat Naik Jabatan')

    current = False
    for i in range(1, 38, 2):
        if i in ilkino.ls_of_generated_random_number :
            current = True
            break

    expected = True

    assert current == expected

def test_random_generator():
    current = MockGenerator.generate()
    expected = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]

    assert current == expected

def test_print_gifted_seat():
    printer = MockPrinter()
    
    current = printer.print_special_ticket('Zola', [2, 3])
    expected = 'Printed Special Ticket'

    assert current == expected

def test_print_normal_seat():
    printer = MockPrinter()
    
    current = printer.print_ticket('Zila', [10, 12])
    expected = 'Printed Ticket'

    assert current == expected