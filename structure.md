ai-data-cleaning-assistant/
│
├── data.db
├── openapi.yml
├── README.md
├── pyproject.toml              # not started
├── .env.example                # not started
├── .gitignore                   # not started
│
├── api/
│   ├── main.py
│   ├── deps.py
│   ├── routes/
│   │   ├── upload.py               # not started
│   │   ├── jobs.py                 
│   │   ├── suggestions.py          # not started 
│   │   └── download.py             # not started
│   ├── schemas/
│   │   ├── request.py
│   │   ├── response.py
│   │   └── domain.py
│   └── middleware/                 # still empty
│       ├── auth.py                 # not started
│       └── rate_limit.py           # not started
│
├── core/
│   ├── config.py                   # not started
│   ├── logging.py                  # not started
│   ├── constants.py
│   └── security.py                 # not started
│
├── services/
│   ├── job_service.py
│   ├── profiling_service.py
│   ├── suggestion_service.py        # not started
│   ├── transform_service.py          # not started
│   └── validation_service.py         # not started
│
├── agents/
│   ├── mcp_client.py                   # not started
│   ├── data_cleaning_agent.py          # not started
│   └── prompts/                        # not started
│       ├── system.md                   # not started
│       ├── suggest_cleaning.md         # not started
│       └── explain_changes.md          # not started
│
├── workflows/                          # not started
│   ├── n8n/                            # not started
│   │   ├── data_profiling.json         # not started
│   │   ├── suggestion_generation.json  # not started
│   │   ├── apply_transformations.json  # not started
│   │   └── full_pipeline.json          # not started
│   └── README.md                       # not started
│
├── storage/
│   ├── db/
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── migrations/          # not started
│   └── object_store.py          # not started
│
├── scripts/                    
│   ├── init_db.py 
│   ├── local_run.py            # not started
│   ├── seed_demo_data.py       # not started
│   └── export_workflow.py      # not started
│
├── tests/                      # not started
│   ├── api/                    # not started
│   ├── services/               # not started
│   └── agents/                 # not started
│
├── docs/                       # not started
│   ├── architecture.md         # not started
│   ├── api.md                  # not started
│   ├── threat_model.md         # not started
│   └── demo_flow.md            # not started
│
└── docker/                     # not started
    ├── Dockerfile              # not started
    ├── docker-compose.yml      # not started
    └── n8n.env                 # not started
