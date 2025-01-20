import { useMountEffect } from "@/hooks/useMountEffect";
import { useSidebarStore } from "@/store/SidebarStore";
import { useWorkflowHasChangesStore } from "@/store/WorkflowHasChangesStore";
import { ReactFlowProvider } from "@xyflow/react";
import { useParams } from "react-router-dom";
import { useWorkflowQuery } from "../hooks/useWorkflowQuery";
import { FlowRenderer } from "./FlowRenderer";
import { getElements } from "./workflowEditorUtils";
import { LogoMinimized } from "@/components/LogoMinimized";
import {
  isDisplayedInWorkflowEditor,
  WorkflowEditorParameterTypes,
  WorkflowParameterTypes,
  WorkflowSettings,
} from "../types/workflowTypes";

function WorkflowEditor() {
  const { workflowPermanentId } = useParams();
  const setCollapsed = useSidebarStore((state) => {
    return state.setCollapsed;
  });
  const setHasChanges = useWorkflowHasChangesStore(
    (state) => state.setHasChanges,
  );

  const { data: workflow, isLoading } = useWorkflowQuery({
    workflowPermanentId,
  });

  useMountEffect(() => {
    setCollapsed(true);
    setHasChanges(false);
  });

  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <LogoMinimized />
      </div>
    );
  }

  if (!workflow) {
    return null;
  }

  const settings: WorkflowSettings = {
    persistBrowserSession: workflow.persist_browser_session,
    proxyLocation: workflow.proxy_location,
    webhookCallbackUrl: workflow.webhook_callback_url,
  };

  const elements = getElements(workflow.workflow_definition.blocks, settings);

  return (
    <div className="h-screen w-full">
      <ReactFlowProvider>
        <FlowRenderer
          initialTitle={workflow.title}
          initialNodes={elements.nodes}
          initialEdges={elements.edges}
          initialParameters={workflow.workflow_definition.parameters
            .filter((parameter) => isDisplayedInWorkflowEditor(parameter))
            .map((parameter) => {
              if (parameter.parameter_type === "workflow") {
                return {
                  key: parameter.key,
                  parameterType: "workflow",
                  dataType: parameter.workflow_parameter_type,
                  defaultValue: parameter.default_value,
                  description: parameter.description,
                };
              } else if (parameter.parameter_type === "context") {
                return {
                  key: parameter.key,
                  parameterType: "context",
                  sourceParameterKey: parameter.source.key,
                  description: parameter.description,
                };
              } else if (
                parameter.parameter_type === "bitwarden_sensitive_information"
              ) {
                return {
                  key: parameter.key,
                  parameterType: "secret",
                  collectionId: parameter.bitwarden_collection_id,
                  identityKey: parameter.bitwarden_identity_key,
                  identityFields: parameter.bitwarden_identity_fields,
                  description: parameter.description,
                };
              } else if (
                parameter.parameter_type ===
                WorkflowParameterTypes.Bitwarden_Credit_Card_Data
              ) {
                return {
                  key: parameter.key,
                  parameterType: WorkflowEditorParameterTypes.CreditCardData,
                  collectionId: parameter.bitwarden_collection_id,
                  itemId: parameter.bitwarden_item_id,
                  description: parameter.description,
                };
              } else {
                return {
                  key: parameter.key,
                  parameterType: "credential",
                  collectionId: parameter.bitwarden_collection_id,
                  urlParameterKey: parameter.url_parameter_key,
                  description: parameter.description,
                };
              }
            })}
          workflow={workflow}
        />
      </ReactFlowProvider>
    </div>
  );
}

export { WorkflowEditor };
