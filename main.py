# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.ast_engine import create_rule, evaluate_rule

app = FastAPI()

# In-memory storage for rules
rules_db = {}

class RuleRequest(BaseModel):
    rule: str

class EvaluateRequest(BaseModel):
    rule_id: int
    data: dict

@app.post("/create_rule/")
def create_rule_endpoint(request: RuleRequest):
    try:
        rule_ast = create_rule(request.rule)
        rule_id = len(rules_db) + 1
        rules_db[rule_id] = rule_ast
        return {"rule_id": rule_id, "ast": repr(rule_ast)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/evaluate_rule/")
def evaluate_rule_endpoint(request: EvaluateRequest):
    try:
        rule_ast = rules_db.get(request.rule_id)
        if not rule_ast:
            raise HTTPException(status_code=404, detail="Rule not found")
        result = evaluate_rule(rule_ast, request.data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
