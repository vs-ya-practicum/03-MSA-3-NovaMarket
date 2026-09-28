# Спринт 3. Задание 3. Масштабирование приложения под нагрузкой

В этой директории находится реализация масштабирования тестового приложения `ghcr.io/yandex-practicum/scaletestapp:latest` в Minikube. Приложение и Locust работают в пространстве имён `scaletestapp`; Prometheus и Prometheus Adapter — в `monitoring`.

## Приложение

Файлы k8s-конфигурации приложения находятся в папке [`deploy/`](./deploy/k8s/scaletestapp)

### Часть 1: масштабирование по памяти

[`deploy/k8s/scaletestapp/hpa-memory.yaml`](deploy/k8s/scaletestapp/hpa-memory.yaml) создаёт HPA `scaletestapp-memory`:

- минимальное количество реплик — `1`;
- максимальное количество реплик — `10`;
- целевая утилизация памяти — `80%`.

Результаты эксперимента сохранены в [`results/hpa-ram`](results/hpa-ram): вывод HPA, состояние Deployment и скриншоты Kubernetes Dashboard, показывающие масштабирование.

#### Нагрузочное тестирование

Locust развёрнут в кластере, поэтому Python и его пакеты не устанавливаются в WSL: См. [`deploy/k8s/loadtest`](deploy/k8s/loadtest) содержит сценарий запросов `GET /`.

Применение конфигурации Locust:

```bash
kubectl apply -k deploy/k8s/loadtest
kubectl port-forward -n scaletestapp service/locust 8089:8089
```

Веб-интерфейс доступен по адресу `http://localhost:8089`.

### Часть 2: масштабирование по RPS

Файлы Helm-конфигурации Prometheus находятся в папке [`deploy/helm`](deploy/helm).

- [`deploy/helm/prometheus-adapter/values.yaml`](deploy/helm/prometheus-adapter/values.yaml) задаёт правило Prometheus Adapter. Оно преобразует `http_requests_total` в пользовательскую метрику Kubernetes `http_requests_per_second` для каждого Pod.
- [`deploy/k8s/scaletestapp/hpa-rps.yaml`](deploy/k8s/scaletestapp/hpa-rps.yaml) создаёт HPA `scaletestapp-rps`, который масштабирует Deployment по средней метрике `http_requests_per_second`. Целевое значение — `20` запросов в секунду на Pod; диапазон реплик — от `1` до `10`.

HPA по памяти и HPA по RPS являются альтернативными вариантами эксперимента. Для каждого запуска применяется только один из них.

Результаты части 2 сохранены в [`results/hpa-rps`](results/hpa-rps):

- [`targets.prometheus.png`](results/hpa-rps/targets.prometheus.png) подтверждает, что Prometheus получает метрики от `scaletestapp`;
- [`graph.prometheus.png`](results/hpa-rps/graph.prometheus.png) показывает метрику `http_requests_total`;
- [`hpa-rps-watch.png`](results/hpa-rps/hpa-rps-watch.png) показывает рост RPS выше целевого значения и масштабирование с одной до трёх реплик.
