# Runbook: Credit Scoring API

## Сервис
- Name: credit-scoring-api
- Namespace: default

---

## Инцидент 1: Сервис недоступен (5xx / timeout)

### Проверка
```bash
kubectl get pods -n default
kubectl describe pod <pod>
kubectl logs <pod>
```

### Решение
```bash
kubectl rollout restart deployment/credit-scoring-api
```

## Инцидент 2: Высокая нагрузка CPU

### Проверка
Grafana → Dashboard → CPU Usage

Prometheus alert: HighCPU

### Решение
```bash
kubectl scale deployment credit-scoring-api --replicas=5
```

## Инцидент 3: Ошибки модели (аномальный ответ)

### Проверка
Логи в Grafana Loki

Проверить MODEL_PATH и ENV

```bash
kubectl describe configmap credit-scoring-config
```

### Решение
```bash
kubectl rollout undo deployment credit-scoring-api
```