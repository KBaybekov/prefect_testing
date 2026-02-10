Использовать настройки кэширования:
prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true

Есть несколько настроек кэширования, которые надо рассмотреть:
Prefect comes prepackaged with a few common cache policies:
DEFAULT: this cache policy uses the task’s inputs, its code definition, as well as the prevailing flow run ID to compute the task’s cache key.
INPUTS: this cache policy uses only the task’s inputs to compute the cache key.
TASK_SOURCE: this cache policy only considers raw lines of code in the task (and not the source code of nested tasks) to compute the cache key.
FLOW_PARAMETERS: this cache policy uses only the parameter values provided to the parent flow run to compute the cache key.
NO_CACHE: this cache policy always returns None and therefore avoids caching and result persistence altogether.

Также надо рассмотреть, как лучше использовать:
хранилище кэша
как лучше конфигурировать key_storage
как настроить изоляцию кэша для concurrency
как использовать Lock в concurrency (есть несколько встроенных менеджеров)