import { describe, it, expect } from 'vitest';

describe('verify testing suite is working', () => {
  it('Guess what', () => {
    expect(true).toBe(true);
  });

  it('testing suite works if this shows up', () => {
    expect(false).toBe(false);
  });
});