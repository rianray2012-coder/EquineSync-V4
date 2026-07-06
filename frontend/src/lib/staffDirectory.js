export const normalizeStaffDirectory = (data) => (Array.isArray(data) ? data : data?.items || []);

export const staffLabel = (staff) => {
  const name = staff?.full_name || staff?.email || staff?.id || "Staff";
  return staff?.role ? `${name} (${String(staff.role).replace(/_/g, " ")})` : name;
};

export const staffOptions = (staff) => staff.map((person) => ({ v: person.id, l: staffLabel(person) }));

export const staffNameById = (staff, id) => {
  const person = staff.find((row) => row.id === id);
  return person?.full_name || person?.email || "";
};
