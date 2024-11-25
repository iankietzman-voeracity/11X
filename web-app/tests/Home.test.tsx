import { render, screen } from "@testing-library/react";
import Home from "../src/Home";

describe("Home", () => {
  it("renders the Home component", () => {
    render(<Home />);
    const title = screen.getByText(/home/i);
    expect(title).toBeDefined();
    expect(title).toBeVisible();
  });
});
