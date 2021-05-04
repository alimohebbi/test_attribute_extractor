package com.benoitletondor.easybudgetapp.view;


import android.support.test.espresso.Espresso;
import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import com.benoitletondor.easybudgetapp.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.action.ViewActions.closeSoftKeyboard;
import static android.support.test.espresso.action.ViewActions.replaceText;
import static android.support.test.espresso.action.ViewActions.swipeLeft;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withClassName;
import static android.support.test.espresso.matcher.ViewMatchers.withContentDescription;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withParent;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class EasyBudgetTest10 {

    @Rule
    public ActivityTestRule<MainActivity> mActivityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Test
    public void easyBudgetTest10() {
        ViewInteraction viewPager1 = onView(
                allOf(withId(R.id.welcome_view_pager),
                        childAtPosition(
                                childAtPosition(
                                        withId(android.R.id.content),
                                        0),
                                0),
                        isDisplayed()));
        viewPager1.perform(swipeLeft());

        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        ViewInteraction appCompatButton1 = onView(
                allOf(withId(R.id.onboarding_screen2_next_button), withText("Go with $"),
                        isDisplayed()));
        appCompatButton1.perform(click());

        ViewInteraction appCompatButton2 = onView(withId(R.id.onboarding_screen3_next_button));
        appCompatButton2.perform(click());

        ViewInteraction appCompatButton3 = onView(
                allOf(withId(R.id.onboarding_screen4_next_button), withText("Let's go!"),
                        isDisplayed()));
        appCompatButton3.perform(click());

        ViewInteraction viewInteraction = onView(
                allOf(withId(R.id.fab_expand_menu_button),
                        childAtPosition(
                                allOf(withId(R.id.fab_choices),
                                        childAtPosition(
                                                withId(R.id.coordinatorLayout),
                                                0)),
                                2),
                        isDisplayed()));
        viewInteraction.perform(click());

        ViewInteraction addFloatingActionButton = onView(
                allOf(withId(R.id.fab_new_expense),
                        childAtPosition(
                                allOf(withId(R.id.fab_choices),
                                        childAtPosition(
                                                withId(R.id.coordinatorLayout),
                                                0)),
                                1),
                        isDisplayed()));
        addFloatingActionButton.perform(click());

        ViewInteraction textInputEditText = onView(
                allOf(withId(R.id.description_edittext),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.description_inputlayout),
                                        0),
                                0),
                        isDisplayed()));
        textInputEditText.perform(replaceText("Entertainment"), closeSoftKeyboard());

        ViewInteraction textInputEditText2 = onView(
                allOf(withId(R.id.amount_edittext),
                        childAtPosition(
                                childAtPosition(
                                        withId(R.id.amount_inputlayout),
                                        0),
                                0),
                        isDisplayed()));
        textInputEditText2.perform(replaceText("45"), closeSoftKeyboard());

        Espresso.pressBack();

        ViewInteraction textView1 = onView(
                allOf(withText("No income or expense yet."),
                        childAtPosition(
                                allOf(withId(R.id.emptyExpensesRecyclerViewPlaceholder),
                                        childAtPosition(
                                                IsInstanceOf.<View>instanceOf(android.widget.LinearLayout.class),
                                                3)),
                                1),
                        isDisplayed()));
        textView1.check(matches(withText("No income or expense yet.")));

    }

    private static Matcher<View> childAtPosition(
            final Matcher<View> parentMatcher, final int position) {

        return new TypeSafeMatcher<View>() {
            @Override
            public void describeTo(Description description) {
                description.appendText("Child at position " + position + " in parent ");
                parentMatcher.describeTo(description);
            }

            @Override
            public boolean matchesSafely(View view) {
                ViewParent parent = view.getParent();
                return parent instanceof ViewGroup && parentMatcher.matches(parent)
                        && view.equals(((ViewGroup) parent).getChildAt(position));
            }
        };
    }
}
