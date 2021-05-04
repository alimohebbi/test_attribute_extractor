package org.openintents.shopping;


import android.support.test.espresso.DataInteraction;
import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static android.support.test.InstrumentationRegistry.getInstrumentation;
import static android.support.test.espresso.Espresso.onData;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.action.ViewActions.closeSoftKeyboard;
import static android.support.test.espresso.action.ViewActions.replaceText;
import static android.support.test.espresso.action.ViewActions.scrollTo;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.isEnabled;
import static android.support.test.espresso.matcher.ViewMatchers.withClassName;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.anything;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class ShoppingListTest11 {

    @Rule
    public ActivityTestRule<ShoppingActivity> mActivityTestRule = new ActivityTestRule<>(ShoppingActivity.class);

    @Test
    public void shoppingListTest11() {
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());

        ViewInteraction textView = onView(
                allOf(withId(android.R.id.title), withText("New list"),
                        isDisplayed()));
        textView.perform(click());

        ViewInteraction editText = onView(
                allOf(withId(R.id.edittext),
                        childAtPosition(
                                childAtPosition(
                                        withId(android.R.id.custom),
                                        0),
                                0),
                        isDisplayed()));
        editText.perform(replaceText("list1"), closeSoftKeyboard());

        ViewInteraction button = onView(
                allOf(withId(android.R.id.button1), withText("OK"),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.ScrollView")),
                                        0),
                                3)));
        button.perform(click());

        ViewInteraction textView2 = onView(withId(android.R.id.text1));
        textView2.check(matches(allOf(withText("list1"), isDisplayed(), isEnabled())));

        ViewInteraction spinner = onView(
                allOf(withId(R.id.spinner_listfilter),
                        childAtPosition(
                                allOf(withId(R.id.filters),
                                        childAtPosition(
                                                withId(R.id.background),
                                                0)),
                                0),
                        isDisplayed()));
        spinner.perform(click());

        DataInteraction checkedTextView = onData(anything())
                .inAdapterView(childAtPosition(
                        withClassName(is("android.widget.PopupWindow$PopupBackgroundView")),
                        0))
                .atPosition(0);
        checkedTextView.perform(click());

        ViewInteraction button2 = onView(
                allOf(withId(R.id.button_add_item), withText("Add"),
                        isDisplayed()));
        button2.perform(click());

        ViewInteraction button3 = onView(
                allOf(withId(R.id.button1), withText("OK"),
                        childAtPosition(
                                allOf(withId(R.id.background),
                                        childAtPosition(
                                                withId(android.R.id.content),
                                                0)),
                                1),
                        isDisplayed()));
        button3.perform(click());

        ViewInteraction autoCompleteTextView = onView(
                allOf(withId(R.id.autocomplete_add_item),
                        childAtPosition(
                                allOf(withId(R.id.add_panel),
                                        childAtPosition(
                                                withId(R.id.background),
                                                3)),
                                0),
                        isDisplayed()));
        autoCompleteTextView.perform(replaceText("item1"), closeSoftKeyboard());

        ViewInteraction button4 = onView(
                allOf(withId(R.id.button_add_item), withText("Add"),
                        isDisplayed()));
        button4.perform(click());

        ViewInteraction textView3 = onView(withId(R.id.name));
        textView3.check(matches(allOf(isDisplayed(), withText("item1"), isEnabled())));

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
