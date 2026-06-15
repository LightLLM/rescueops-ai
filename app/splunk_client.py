import os
import time
from typing import List, Dict, Any

import splunklib.client as client
import splunklib.results as results
from dotenv import load_dotenv

load_dotenv()


class SplunkClient:
    """Small Splunk SDK wrapper for RescueOps AI."""

    def __init__(self):
        self.index = os.getenv("SPLUNK_INDEX", "rescueops")
        self.service = client.connect(
            host=os.getenv("SPLUNK_HOST", "localhost"),
            port=int(os.getenv("SPLUNK_PORT", "8089")),
            username=os.getenv("SPLUNK_USERNAME"),
            password=os.getenv("SPLUNK_PASSWORD"),
            scheme="https",
        )

    def search(self, query: str) -> List[Dict[str, Any]]:
        if not query.strip().startswith("search"):
            query = "search " + query

        job = self.service.jobs.create(query)
        while not job.is_done():
            time.sleep(0.4)

        reader = results.ResultsReader(job.results(output_mode="json"))
        output = []
        for item in reader:
            if isinstance(item, dict):
                output.append(dict(item))
        return output

    def incident_error_summary(self):
        return self.search(
            f'''
            index={self.index} level=ERROR
            | stats count avg(latency_ms) max(latency_ms) by service endpoint deployment_version
            | sort - count
            '''
        )

    def incident_timeline(self):
        return self.search(
            f'''
            index={self.index}
            | bin _time span=5m
            | stats count as events,
                    count(eval(level="ERROR")) as errors,
                    avg(latency_ms) as avg_latency
              by _time service
            | sort _time
            '''
        )

    def deployment_events(self):
        return self.search(
            f'''
            index={self.index} message="deployment completed for checkout-api"
            | table _time service deployment_version message
            '''
        )

    def high_latency_services(self):
        return self.search(
            f'''
            index={self.index} latency_ms>1000
            | stats count avg(latency_ms) max(latency_ms) by service deployment_version
            | sort - avg(latency_ms)
            '''
        )
