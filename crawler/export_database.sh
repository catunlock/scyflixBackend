#!/bin/bash
mongoexport -db database --collection papers --out papers.json
mongoexport -db database --collection clusters --out clusters.json
