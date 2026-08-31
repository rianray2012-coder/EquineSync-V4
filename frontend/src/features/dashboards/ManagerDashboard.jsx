import Dashboard from "../../pages/Dashboard";
import TrustWorkflowPanel from "../../components/TrustWorkflowPanel";

export default function ManagerDashboard() {
  return (
    <>
      <TrustWorkflowPanel roleKey="manager" testid="manager-north-star" />
      <Dashboard />
    </>
  );
}
