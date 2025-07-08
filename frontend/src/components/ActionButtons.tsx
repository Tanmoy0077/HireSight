import { Eye, ClipboardList, BookOpen } from "lucide-react";

interface ActionButtonsProps {
  onOpenInterview: () => void;
  onOpenRec: () => void;
  onOpenDev: () => void;
}

export default function ActionButtons({
  onOpenInterview,
  onOpenRec,
  onOpenDev,
}: ActionButtonsProps) {
  return (
    <div className="flex flex-col gap-4 justify-center">
      <button
        onClick={onOpenInterview}
        className="border border-blue-600 text-blue-600 hover:bg-blue-50 px-4 py-3 rounded-lg w-full flex items-center gap-2 justify-center font-semibold shadow-sm transition-colors"
      >
        <Eye /> View Interview Prep
      </button>
      <button
        onClick={onOpenRec}
        className="border border-green-600 text-green-600 hover:bg-green-50 px-4 py-3 rounded-lg w-full flex items-center gap-2 justify-center font-semibold shadow-sm transition-colors"
      >
        <ClipboardList /> Recommendations
      </button>
      <button
        onClick={onOpenDev}
        className="border border-amber-600 text-amber-600 hover:bg-amber-50 px-4 py-3 rounded-lg w-full flex items-center gap-2 justify-center font-semibold shadow-sm transition-colors"
      >
        <BookOpen /> Development Plan
      </button>
    </div>
  );
}
