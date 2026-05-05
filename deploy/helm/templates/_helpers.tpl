{{/*
Expand the name of the chart.
*/}}
{{- define "incident-mcp.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a fully qualified app name.
*/}}
{{- define "incident-mcp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := .Chart.Name }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "incident-mcp.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | quote }}
{{ include "incident-mcp.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "incident-mcp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "incident-mcp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Name of the Secret holding ServiceNow credentials.
Uses existingSecret if provided, otherwise the chart-managed secret.
*/}}
{{- define "incident-mcp.secretName" -}}
{{- if .Values.servicenow.existingSecret }}
{{- .Values.servicenow.existingSecret }}
{{- else }}
{{- include "incident-mcp.fullname" . }}
{{- end }}
{{- end }}
