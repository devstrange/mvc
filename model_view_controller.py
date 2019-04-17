# model_view_controller.py
import basic_backend
import mvc_exceptions as mvc_exc


# Model
# business logic
# View 나 Controller 에 의존하지 않음
class ModelBasic(object):

    def __init__(self, application_items):
        self._item_type = 'product'
        self.create_items(application_items)

    @property
    def item_type(self):
        return self._item_type

    @item_type.setter
    def item_type(self, new_item_type):
        self._item_type = new_item_type

    def create_item(self, name, price, quantity):
        basic_backend.create_item(name, price, quantity)

    def create_items(self, items):
        basic_backend.create_items(items)

    def read_item(self, name):
        return basic_backend.read_item(name)

    def read_items(self):
        return basic_backend.read_items()

    def update_item(self, name, price, quantity):
        basic_backend.update_item(name, price, quantity)

    def delete_item(self, name):
        basic_backend.delete_item(name)


# view
# 모든 메소드가 staticmethod
# Model 과 Controller 에 의존하지 않음
class View(object):

    @staticmethod
    def show_bullet_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for item in items:
            print('* {}'.format(item))

    @staticmethod
    def show_number_point_list(item_type, items):
        print('--- {} LIST ---'.format(item_type.upper()))
        for i, item in enumerate(items):
            print('{}. {}'.format(i+1, item))

    @staticmethod
    def show_item(item_type, item, item_info):
        print('/' * 61)
        print('Good news, we have some {}!'.format(item.upper()))
        print('{} INFO: {}'.format(item_type.upper(), item_info))
        print('/' * 61)

    @staticmethod
    def display_missing_item_error(item, err):
        print('*' * 61)
        print('We are sorry, we have no {}!'.format(item.upper()))
        print('{}'.format(err.args[0]))
        print('*' * 61)

    @staticmethod
    def display_item_already_stored_error(item, item_type, err):
        print('*' * 61)
        print('Hey! We already have {} in our {} list!'
            .format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('*' * 61)

    @staticmethod
    def display_item_not_yet_stored_error(item, item_type, err):
        print('*' * 61)
        print('We don\'t have any {} in our {} list. Please insert in first!'
            .format(item.upper(), item_type))
        print('{}'.format(err.args[0]))
        print('*' * 61)

    @staticmethod
    def display_item_stored(item, item_type):
        print('+' * 61)
        print('Hooray! We have just added some {} to our {} list!'
            .format(item.upper(), item_type))
        print('+' * 61)

    @staticmethod
    def display_change_item_type(older, newer):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change item type form "{}" to "{}"'.format(older, newer))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_updated(item, o_price, o_quantity, n_price, n_quantity):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('Change {} price: {} --> {}'
            .format(item, o_price, n_price))
        print('Change {} quantity: {} --> {}'
            .format(item, o_quantity, n_quantity))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')

    @staticmethod
    def display_item_deletion(name):
        print('-' * 61)
        print('We have just removed {} from our list'.format(name))
        print('-' * 61)


# Controller
# Model 과 View 를 참조
# Controller는 사용자 입력을 받아드리고
# 데이터 표현은 View에게,
# 데이터 핸들링은 Model에게 위임한다
class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self, bullet_points=False):
        items = self.model.read_items()
        item_type = self.model.item_type
        if bullet_points:
            self.view.show_bullet_point_list(item_type, items)
        else:
            self.view.show_number_point_list(item_type, items)

    def show_item(self, item_name):
        try:
            item = self.model.read_item(item_name)
            item_type = self.model.item_type
            self.view.show_item(item_type, item_name, item)
        except mvc_exc.ItemNotStored as e:
            self.view.display_missing_item_error(item_name, e)


def main():
    my_items = [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'milk', 'price': 1.0, 'quantity': 10},
        {'name': 'wine', 'price': 10.0, 'quantity': 5},
    ]

    c = Controller(ModelBasic(my_items), View())
    c.show_items()
    c.show_items(bullet_points=True)
    c.show_item('chocolate')
    c.show_item('bread')


if __name__ == '__main__':
    main()
