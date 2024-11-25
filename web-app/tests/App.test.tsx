import { render, screen } from "@testing-library/react";
import App from "../src/App";

describe("App", () => {
  beforeEach(() => {
    render(<App></App>);
  });
  it("renders the top level navigation", async () => {
    const layout = screen.getByRole("navigation");
    expect(layout).toBeVisible();
  });
});
