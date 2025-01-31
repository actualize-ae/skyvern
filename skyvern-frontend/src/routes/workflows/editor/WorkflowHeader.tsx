import { SaveIcon } from "@/components/icons/SaveIcon";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  ChevronDownIcon,
  ChevronUpIcon,
  PlayIcon,
} from "@radix-ui/react-icons";
import { useNavigate, useParams } from "react-router-dom";
import { useGlobalWorkflowsQuery } from "../hooks/useGlobalWorkflowsQuery";
import { EditableNodeTitle } from "./nodes/components/EditableNodeTitle";

type Props = {
  title: string;
  parametersPanelOpen: boolean;
  onParametersClick: () => void;
  onSave: () => void;
  onTitleChange: (title: string) => void;
};

function WorkflowHeader({
  title,
  parametersPanelOpen,
  onParametersClick,
  onSave,
  onTitleChange,
}: Props) {
  const { workflowPermanentId } = useParams();
  const { data: globalWorkflows } = useGlobalWorkflowsQuery();
  const navigate = useNavigate();

  if (!globalWorkflows) {
    return null; // this should be loaded already by some other components
  }

  const isGlobalWorkflow = globalWorkflows.some(
    (workflow) => workflow.workflow_permanent_id === workflowPermanentId,
  );

  return (
    <div className="flex h-full w-full justify-between rounded-xl bg-slate-elevation2 px-6 py-5">
      <div className="flex h-full items-center">
        <EditableNodeTitle
          editable={true}
          onChange={onTitleChange}
          value={title}
          titleClassName="text-3xl"
          inputClassName="text-3xl"
        />
      </div>
      <div className="flex h-full items-center justify-end gap-4">
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                size="icon"
                variant="tertiary"
                className="size-10"
                disabled={isGlobalWorkflow}
                onClick={() => {
                  onSave();
                }}
              >
                <SaveIcon />
              </Button>
            </TooltipTrigger>
            <TooltipContent>Save</TooltipContent>
          </Tooltip>
        </TooltipProvider>
        <Button variant="tertiary" size="lg" onClick={onParametersClick}>
          <span className="mr-2">Parameters</span>
          {parametersPanelOpen ? (
            <ChevronUpIcon className="h-6 w-6" />
          ) : (
            <ChevronDownIcon className="h-6 w-6" />
          )}
        </Button>
        <Button
          size="lg"
          onClick={() => {
            navigate(`/workflows/${workflowPermanentId}/run`);
          }}
        >
          <PlayIcon className="mr-2 h-6 w-6" />
          Run
        </Button>
      </div>
    </div>
  );
}

export { WorkflowHeader };
