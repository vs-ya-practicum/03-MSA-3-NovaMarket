# Спринт 3 Задание 1

- [EDA-Архитектура](#eda-архитектура)
- [События](#события)
- [Сценарий оформления заказа](#сценарий-оформления-заказа)
  - [Диаграммы](#диаграммы)
  - [Реестры событий Saga-хореографии оформления заказа](#реестры-событий-saga-хореографии-оформления-заказа)
    - [Успешный сценарий оформления заказа](#успешный-сценарий-оформления-заказа)
    - [Ошибочные сценарии оформления заказа](#ошибочные-сценарии-оформления-заказа)

---

## EDA-Архитектура

<details>
<summary>Событийная архитектура NovaMarket Container</summary>

![Диаграмма: Событийная архитектура NovaMarket Container](diagrams/.svg/novamarket.container.c4.svg)

</details>

## События

- [Реестр событий системы](./all-events-registry.md)

## Сценарий оформления заказа

### Диаграммы

<details>
<summary>Успешное оформление заказа — Saga-хореография Sequence</summary>

![Успешное оформление заказа — Saga-хореография Sequence](diagrams/.svg/SEQ-01-order-checkout-saga-success.sequence.svg)

</details>

<details>
<summary>Ошибочные сценарии оформления заказа — Saga-хореография Sequence</summary>

![Ошибочные сценарии оформления заказа — Saga-хореография Sequence](diagrams/.svg/SEQ-02-order-checkout-saga-failure.sequence.svg)

</details>

### Реестры событий Saga-хореографии оформления заказа

В реестры включены события, которые запускают шаг Saga или определяют её результат.

#### Успешный сценарий оформления заказа

| Этап                   | Тип события | Название                 |
| ---------------------- | ----------- | ------------------------ |
| Подтверждение заказа   | domain      | `OrderConfirmedEvent`    |
| Резервирование товаров | domain      | `InventoryReservedEvent` |
| Инициирование оплаты   | domain      | `PaymentInitiatedEvent`  |
| Успешная оплата        | domain      | `PaymentSucceededEvent`  |

#### Ошибочные сценарии оформления заказа

| Этап                                 | Тип события  | Название                                 |
| ------------------------------------ | ------------ | ---------------------------------------- |
| Подтверждение заказа                 | domain       | `OrderConfirmedEvent`                    |
| Недостаток товара при резервировании | failure      | `InventoryReservationFailedEvent`        |
| Резервирование товаров               | domain       | `InventoryReservedEvent`                 |
| Инициирование оплаты                 | domain       | `PaymentInitiatedEvent`                  |
| Ошибка оплаты                        | failure      | `PaymentFailedEvent`                     |
| Отмена заказа после ошибки оплаты    | compensation | `OrderCancelledAfterPaymentFailureEvent` |
| Освобождение резерва                 | domain       | `InventoryReservationReleasedEvent`      |
