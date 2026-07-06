import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { resolveDashboardPath } from "../../lib/roleLanding";

export default function DashboardResolver() {
  const { user } = useAuth();
  return <Navigate to={resolveDashboardPath(user)} replace />;
}
