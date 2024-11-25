import { render, screen, waitFor } from "@testing-library/react";
import Dashboard from "../src/Dashboard";

describe("Dashboard", () => {
  beforeEach(() => {
    render(<Dashboard />);
  });
  it("renders the Dashboard component", async () => {
    await waitFor(() => {
      const title = screen.getByText(/dashboard/i);
      expect(title).toBeDefined();
      expect(title).toBeVisible();
    });
  });
  it("build the cell matrix table", async () => {
    await waitFor(() => {
      const rows = screen.getAllByRole("row");
      console.log(rows);
      expect(rows).toBeDefined();
      expect(rows).toHaveLength(10);
    });
  });
});
