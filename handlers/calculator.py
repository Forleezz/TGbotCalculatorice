import math
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart

calculator_router = Router()


class CalculatorState(StatesGroup):
    first_number = State()
    operator = State()
    second_number = State()


@calculator_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.reply('Hello this is a calculator. Click /calculate to start.')


@calculator_router.message(F.text.startswith("/calculate"))
async def start_calculation(message: types.Message, state: FSMContext):
    await message.answer('Enter the first number:')
    await state.set_state(CalculatorState.first_number)


@calculator_router.message(CalculatorState.first_number, F.text)
async def get_first_number(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Please enter a valid number:')
        return
    await state.update_data(first_number=int(message.text))
    await message.answer('Choose an operator (+, -, *, /):')
    await state.set_state(CalculatorState.operator)


@calculator_router.message(CalculatorState.operator, F.text)
async def get_operator(message: types.Message, state: FSMContext):
    if message.text not in ['+', '-', '*', '/']:
        await message.answer('Please choose a valid operator (+, -, *, /):')
        return
    await state.update_data(operator=message.text)
    await message.answer('Enter the second number:')
    await state.set_state(CalculatorState.second_number)


@calculator_router.message(CalculatorState.second_number, F.text)
async def get_second_number(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Please enter a valid number:')
        return
    data = await state.get_data()
    first_number = data['first_number']
    operator = data['operator']
    second_number = int(message.text)

    try:
        if operator == '+':
            result = first_number + second_number
        elif operator == '-':
            result = first_number - second_number
        elif operator == '*':
            result = first_number * second_number
        elif operator == '/':
            result = first_number / second_number
        await message.answer(f'Result: {result}')
    except ZeroDivisionError:
        await message.answer('Division by zero is not allowed.')

    await state.clear()
