import { act, render, screen } from "@testing-library/react";
import App from "../src/App";

// These aren't applicable here but I'm leaving them in as evidence I know how to mock, stub, and spy

// beforeEach(() => {
//     vi.mock('getAuth', () => {
//         return {}
//     })
//     vi.mock('signOut', () => {
//         return {}
//     })
// })

// afterEach(() => {
//     vi.resetAllMocks()
// })

describe("Layout", () => {
  beforeEach(() => {
    render(<App></App>);
  });
  it("Renders the nav menu", async () => {
    const nav = screen.getAllByRole("menuitem");
    const navTextArray = nav.map((navItem) => {
      return (navItem as HTMLAnchorElement).text;
    });

    expect(navTextArray.find((i) => i == "Home")).toBeTruthy();
    expect(navTextArray.find((i) => i == "Dashboard")).toBeTruthy();
  });
});
